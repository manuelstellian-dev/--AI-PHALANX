"""
polis.yamlite — YAML subset parser and emitter (replaces PyYAML).

Supported (everything the project's configuration uses):
- block mappings and block sequences (including "- key: value" items)
- flow sequences [a, b] and flow mappings {k: v} (single line)
- scalars: plain, 'single-quoted', "double-quoted" (with escapes), null/~,
  true/false, integers (incl. 0x/0o), floats (incl. .inf/.nan)
- literal (|) and folded (>) block scalars, with -/+ chomping
- comments, blank lines, a leading '---' document marker

Booleans follow YAML 1.2 (only true/false), so a key like `on:` stays the
string "on". This is a deliberate difference from PyYAML's YAML 1.1 behaviour.

API: safe_load(text_or_stream), safe_dump(data, stream=None, ...), dump = safe_dump.
"""

import math
import re
from typing import Any, List, Optional, Tuple


class YAMLError(ValueError):
    """Raised on malformed or unsupported YAML."""


_INT_RE = re.compile(r"^[-+]?(0|[1-9][0-9_]*)$")
_HEX_RE = re.compile(r"^0x[0-9a-fA-F_]+$")
_OCT_RE = re.compile(r"^0o[0-7_]+$")
_FLOAT_RE = re.compile(r"^[-+]?(\.[0-9]+|[0-9][0-9_]*(\.[0-9_]*)?)([eE][-+]?[0-9]+)?$")
_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "0": "\0", '"': '"', "\\": "\\", "/": "/", " ": " ", "a": "\a",
            "b": "\b", "e": "\x1b", "f": "\f", "v": "\v"}


def _strip_comment(line: str) -> str:
    """Remove a trailing comment that is outside quotes."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                if quote == "'" and line[i + 1:i + 2] == "'":
                    continue
                quote = None
            elif ch == "\\" and quote == '"':
                continue
        elif ch in "'\"":
            if i == 0 or line[i - 1] in " \t[{,:-":
                quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i].rstrip()
    return line.rstrip()


def _parse_double_quoted(text: str) -> str:
    out, i = [], 1
    while i < len(text) - 1:
        ch = text[i]
        if ch == "\\":
            nxt = text[i + 1]
            if nxt == "x":
                out.append(chr(int(text[i + 2:i + 4], 16)))
                i += 4
                continue
            if nxt == "u":
                out.append(chr(int(text[i + 2:i + 6], 16)))
                i += 6
                continue
            out.append(_ESCAPES.get(nxt, nxt))
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def parse_scalar(text: str) -> Any:
    """Convert a scalar token to its Python value."""
    text = text.strip()
    if text == "":
        return None
    if len(text) >= 2 and text[0] == text[-1] == '"':
        return _parse_double_quoted(text)
    if len(text) >= 2 and text[0] == text[-1] == "'":
        return text[1:-1].replace("''", "'")
    if text[0] == "[" and text[-1] == "]":
        return [parse_scalar(item) for item in _split_flow(text[1:-1])]
    if text[0] == "{" and text[-1] == "}":
        result = {}
        for item in _split_flow(text[1:-1]):
            key, sep, value = _split_key(item)
            if not sep:
                raise YAMLError(f"Invalid flow mapping item: {item!r}")
            result[parse_scalar(key)] = parse_scalar(value)
        return result
    lowered = text.lower()
    if lowered in ("null", "~"):
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if _INT_RE.match(text):
        return int(text.replace("_", ""))
    if _HEX_RE.match(text):
        return int(text, 16)
    if _OCT_RE.match(text):
        return int(text, 8)
    if lowered in (".inf", "+.inf"):
        return math.inf
    if lowered == "-.inf":
        return -math.inf
    if lowered == ".nan":
        return math.nan
    if _FLOAT_RE.match(text) and any(c in text for c in ".eE"):
        return float(text.replace("_", ""))
    return text


def _split_flow(body: str) -> List[str]:
    """Split a flow collection body on top-level commas."""
    items, depth, quote, start = [], 0, None, 0
    for i, ch in enumerate(body):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        elif ch == "," and depth == 0:
            items.append(body[start:i])
            start = i + 1
    tail = body[start:]
    if tail.strip():
        items.append(tail)
    return [item.strip() for item in items if item.strip()]


def _split_key(text: str) -> Tuple[str, str, str]:
    """Split 'key: value' on the first top-level ': ' (or trailing ':')."""
    quote, depth = None, 0
    for i, ch in enumerate(text):
        if quote:
            if ch == quote:
                quote = None
            continue
        if ch in "'\"" and i == 0:
            quote = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        elif ch == ":" and depth == 0 and (i + 1 == len(text) or text[i + 1] in " \t"):
            return text[:i].strip(), ":", text[i + 1:].strip()
    return text, "", ""


class _Parser:
    def __init__(self, text: str):
        self.raw_lines = text.splitlines()
        self.lines: List[Tuple[int, int, str]] = []  # (raw index, indent, content)
        for idx, raw in enumerate(self.raw_lines):
            if "\t" in raw[:len(raw) - len(raw.lstrip())]:
                raise YAMLError(f"Tabs are not allowed for indentation (line {idx + 1})")
            content = _strip_comment(raw)
            if not content.strip() or content.strip() in ("---", "..."):
                continue
            self.lines.append((idx, len(content) - len(content.lstrip(" ")), content.strip()))
        self.pos = 0

    def parse(self) -> Any:
        if not self.lines:
            return None
        value = self._block(self.lines[0][1])
        if self.pos < len(self.lines):
            raise YAMLError(f"Unexpected content at line {self.lines[self.pos][0] + 1}")
        return value

    def _block(self, indent: int) -> Any:
        if self.lines[self.pos][2].startswith("- ") or self.lines[self.pos][2] == "-":
            return self._sequence(indent)
        return self._mapping(indent)

    def _value_after(self, rest: str, parent_indent: int, raw_idx: int) -> Any:
        """Value following 'key:' or '- ': inline scalar, block scalar, or nested block."""
        if rest and rest[0] in "|>":
            return self._block_scalar(rest, parent_indent, raw_idx)
        if rest:
            return parse_scalar(rest)
        if self.pos < len(self.lines) and self.lines[self.pos][1] > parent_indent:
            return self._block(self.lines[self.pos][1])
        if (self.pos < len(self.lines) and self.lines[self.pos][1] == parent_indent
                and self.lines[self.pos][2].startswith("- ")):
            # YAML allows a sequence at the same indent as its parent key
            return self._sequence(parent_indent)
        return None

    def _mapping(self, indent: int) -> dict:
        result = {}
        while self.pos < len(self.lines):
            raw_idx, ind, content = self.lines[self.pos]
            if ind < indent:
                break
            if ind > indent:
                raise YAMLError(f"Bad indentation at line {raw_idx + 1}")
            if content.startswith("- "):
                break
            key, sep, rest = _split_key(content)
            if not sep:
                raise YAMLError(f"Expected 'key: value' at line {raw_idx + 1}: {content!r}")
            self.pos += 1
            result[parse_scalar(key)] = self._value_after(rest, indent, raw_idx)
        return result

    def _sequence(self, indent: int) -> list:
        result = []
        while self.pos < len(self.lines):
            raw_idx, ind, content = self.lines[self.pos]
            if ind != indent or not (content.startswith("- ") or content == "-"):
                if ind > indent:
                    raise YAMLError(f"Bad indentation at line {raw_idx + 1}")
                break
            item = content[2:].strip() if content != "-" else ""
            self.pos += 1
            key, sep, rest = _split_key(item) if item and item[0] not in "[{'\"" else (item, "", "")
            if sep:
                # "- key: value" starts a mapping whose keys align after the dash
                child_indent = indent + 2
                mapping = {parse_scalar(key): self._value_after(rest, child_indent, raw_idx)}
                if self.pos < len(self.lines) and self.lines[self.pos][1] == child_indent \
                        and not self.lines[self.pos][2].startswith("- "):
                    mapping.update(self._mapping(child_indent))
                result.append(mapping)
            else:
                result.append(self._value_after(item, indent, raw_idx))
        return result

    def _block_scalar(self, header: str, parent_indent: int, raw_idx: int) -> str:
        style, chomp = header[0], header[1:2]
        body: List[str] = []
        block_indent: Optional[int] = None
        i = raw_idx + 1
        while i < len(self.raw_lines):
            line = self.raw_lines[i]
            if line.strip():
                ind = len(line) - len(line.lstrip(" "))
                if ind <= parent_indent:
                    break
                if block_indent is None:
                    block_indent = ind
                body.append(line[block_indent:])
            else:
                body.append("")
            i += 1
        while self.pos < len(self.lines) and self.lines[self.pos][0] < i:
            self.pos += 1
        while body and body[-1] == "" and chomp != "+":
            body.pop()
        if style == "|":
            text = "\n".join(body)
        else:
            text = re.sub(r"(?<!\n)\n(?!\n)", " ", "\n".join(body))
        if chomp == "-":
            return text
        return text + "\n" if text else text


def safe_load(stream: Any) -> Any:
    """Parse YAML from a string or a readable stream."""
    text = stream.read() if hasattr(stream, "read") else stream
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    return _Parser(text).parse()


# ----------------------------------------------------------------- emitter

def _needs_quotes(text: str) -> bool:
    return (text == "" or text != text.strip() or parse_scalar(text) != text
            or any(c in text for c in ":#{}[],&*!|>'\"%@`\n") or text[0] in "-?")


def _scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return repr(value)
    text = str(value)
    if _needs_quotes(text):
        return "'" + text.replace("'", "''") + "'"
    return text


def _emit(value: Any, indent: int, out: List[str], sort_keys: bool) -> None:
    pad = " " * indent
    if isinstance(value, dict):
        if not value:
            out.append(pad + "{}")
        items = sorted(value.items(), key=lambda kv: str(kv[0])) if sort_keys else value.items()
        for key, val in items:
            if isinstance(val, (dict, list)) and val:
                out.append(f"{pad}{_scalar(key)}:")
                _emit(val, indent + 2 if isinstance(val, dict) else indent, out, sort_keys)
            else:
                rendered = "[]" if val == [] else ("{}" if val == {} else _scalar(val))
                out.append(f"{pad}{_scalar(key)}: {rendered}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)) and item:
                sub: List[str] = []
                _emit(item, indent + 2, sub, sort_keys)
                out.append(pad + "- " + sub[0].lstrip())
                out.extend(sub[1:])
            else:
                out.append(pad + "- " + _scalar(item))
    else:
        out.append(pad + _scalar(value))


def safe_dump(data: Any, stream: Any = None, default_flow_style: bool = False,
              sort_keys: bool = True, **_ignored) -> Optional[str]:
    """
    Serialize data (dict / list / scalars) to block-style YAML.

    Returns:
        The YAML text when no stream is given
    """
    lines: List[str] = []
    _emit(data, 0, lines, sort_keys)
    text = "\n".join(lines) + "\n"
    if stream is None:
        return text
    stream.write(text)
    return None


dump = safe_dump

__all__ = ["safe_load", "safe_dump", "dump", "YAMLError", "parse_scalar"]

