"""
Tests for polis, the sovereign foundation (LAW-015, DEC-022).

Every module is verified against fixed expectations (no external oracle at
test time): YAML parsing of the repository's real files, /proc sensing on the
live host, graph semantics, logging sinks, and, project-wide, the absence of
any third-party import.
"""

import ast
import glob
import io
import logging
import math
import os
import socket
import sys
import time

import pytest

from polis import graph, sysinfo, yamlite
from polis.log import Logger, parse_days, parse_size

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOCAL_PACKAGES = {'api', 'core', 'control', 'phalanx', 'hoplites', 'vault', 'sparta', 'logos',
                  'mnemosyne', 'parallel_execution', 'polis', 'tests', 'audit_analyzer',
                  'autonomous_audit_agent'}

# Libraries not yet replaced during the sovereignty migration (DEC-022).
# This set may only shrink; LAW-015 is fully met when it is empty.
PENDING = {'numpy', 'scipy', 'fastapi', 'pydantic', 'uvicorn', 'httpx', 'pytest'}


def _third_party_imports():
    stdlib = set(sys.stdlib_module_names)
    found = {}
    for path in glob.glob(os.path.join(REPO_ROOT, '**', '*.py'), recursive=True):
        rel = os.path.relpath(path, REPO_ROOT)
        if rel.startswith(('.', 'sparta-env', 'venv')):
            continue
        with open(path, encoding='utf-8') as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module]
            else:
                continue
            for name in names:
                top = name.split('.')[0]
                if top not in stdlib and top not in LOCAL_PACKAGES:
                    found.setdefault(top, set()).add(rel)
    return found


def test_no_third_party_imports():
    """LAW-015: only the standard library and our own packages are imported."""
    found = _third_party_imports()
    unexpected = {lib: sorted(files) for lib, files in found.items() if lib not in PENDING}
    assert unexpected == {}, unexpected
    # The optional external embedding backend is imported lazily by name only
    assert 'sentence_transformers' not in found


def test_pending_set_only_contains_libraries_still_in_use():
    """The migration ledger is honest: every pending library is still really imported."""
    found = _third_party_imports()
    assert PENDING <= set(found) | {'pytest'}, sorted(PENDING - set(found))


# ---------------------------------------------------------------- yamlite

class TestYamlite:

    def test_repository_settings_parse(self):
        with open(os.path.join(REPO_ROOT, 'config', 'settings.yaml'), encoding='utf-8') as f:
            cfg = yamlite.safe_load(f)
        assert cfg['system']['name'] == 'ΛΕΩΝΙΔΑΣ-AI PHALANX'
        assert cfg['phalanx']['thermopylae']['vault_path'] == ['/data/vault', '/data/encrypted_vault']
        assert cfg['phalanx']['thermopylae']['thermopylae_armed'] is False
        assert cfg['hardware']['npu_allocation']['decision_engine'] == 15
        assert cfg['phalanx']['agoge']['adaptation_range'] == [0.5, 2.0]
        assert cfg['hoplites']['weapon_master']['allowed_domains'] == []

    def test_compose_and_workflow_parse(self):
        with open(os.path.join(REPO_ROOT, 'docker-compose.yml'), encoding='utf-8') as f:
            compose = yamlite.safe_load(f)
        assert compose['services']['leonidas-core']['ports'] == ['7300:7300']
        with open(os.path.join(REPO_ROOT, '.github', 'workflows', 'ci.yml'), encoding='utf-8') as f:
            ci = yamlite.safe_load(f)
        assert 'on' in ci  # YAML 1.2: `on` is a string key, not True
        assert ci['jobs']['test']['runs-on'] == 'ubuntu-latest'

    @pytest.mark.parametrize("text,expected", [
        ('a: "x\\ty"', {'a': 'x\ty'}),
        ("a: 'it''s'", {'a': "it's"}),
        ('a: 0x1F', {'a': 31}),
        ('a: 0o17', {'a': 15}),
        ('a: 1_000', {'a': 1000}),
        ('a: -2.5e3', {'a': -2500.0}),
        ('a: ~', {'a': None}),
        ('a: true', {'a': True}),
        ('a: yes', {'a': 'yes'}),          # YAML 1.2
        ('a: [1, "b", {c: 2}]', {'a': [1, 'b', {'c': 2}]}),
        ('a: x # comment', {'a': 'x'}),
        ('a: "# not a comment"', {'a': '# not a comment'}),
        ('url: http://host:80/p', {'url': 'http://host:80/p'}),
    ])
    def test_scalars(self, text, expected):
        assert yamlite.safe_load(text) == expected

    def test_special_floats(self):
        out = yamlite.safe_load("a: .inf\nb: -.inf\nc: .nan")
        assert out['a'] == math.inf and out['b'] == -math.inf and math.isnan(out['c'])

    def test_block_structures(self):
        text = (
            "---\n"
            "list:\n"
            "  - one\n"
            "  - key: v\n"
            "    other: 2\n"
            "same_indent:\n"
            "- a\n"
            "- b\n"
            "literal: |\n"
            "  line 1\n"
            "  line 2\n"
            "folded: >-\n"
            "  word\n"
            "  more\n"
            "empty:\n"
        )
        assert yamlite.safe_load(text) == {
            'list': ['one', {'key': 'v', 'other': 2}],
            'same_indent': ['a', 'b'],
            'literal': 'line 1\nline 2\n',
            'folded': 'word more',
            'empty': None,
        }

    def test_round_trip(self):
        data = {'k': 'ab' * 32, 'n': 3, 'f': 0.95, 'b': True, 'none': None,
                'lst': ['/data/vault', 'x: y', "it's"], 'nested': {'a': [{'k': 1, 'j': 'two'}], 'e': []}}
        assert yamlite.safe_load(yamlite.safe_dump(data, sort_keys=False)) == data
        stream = io.StringIO()
        yamlite.dump(data, stream)
        assert yamlite.safe_load(stream.getvalue()) == data

    @pytest.mark.parametrize("bad", ["a: 1\n   b: 2", "\tkey: 1", "just text\nmore: 1"])
    def test_errors(self, bad):
        with pytest.raises(yamlite.YAMLError):
            yamlite.safe_load(bad)


# ---------------------------------------------------------------- sysinfo

class TestSysinfo:

    def test_cpu(self):
        assert sysinfo.cpu_count() >= 1
        value = sysinfo.cpu_percent(interval=0.05)
        assert 0.0 <= value <= 100.0
        assert 0.0 <= sysinfo.cpu_percent() <= 100.0  # non-blocking mode

    def test_memory_and_disk(self):
        mem = sysinfo.virtual_memory()
        assert mem.total > 0 and 0 <= mem.available <= mem.total
        assert 0.0 <= mem.percent <= 100.0
        disk = sysinfo.disk_usage('/')
        assert disk.total > 0 and 0.0 <= disk.percent <= 100.0

    @pytest.mark.parametrize("hex_addr,family,expected", [
        ("0100007F:1F90", socket.AF_INET, ("127.0.0.1", 8080)),
        ("00000000:0035", socket.AF_INET, ("0.0.0.0", 53)),
        ("00000000000000000000000001000000:01BB", socket.AF_INET6, ("::1", 443)),
    ])
    def test_address_decoding(self, hex_addr, family, expected):
        assert tuple(sysinfo._decode_address(hex_addr, family)) == expected

    @pytest.mark.skipif(not sys.platform.startswith('linux'), reason="/proc is Linux-specific")
    def test_detects_a_live_connection(self):
        server = socket.socket()
        server.bind(('127.0.0.1', 0))
        server.listen()
        port = server.getsockname()[1]
        client = socket.create_connection(('127.0.0.1', port))
        accepted, _ = server.accept()
        try:
            time.sleep(0.05)
            conns = sysinfo.net_connections('tcp')
            assert any(c.laddr.port == port and c.status == 'LISTEN' for c in conns)
            assert any(c.raddr and c.raddr.port == port and c.status == 'ESTABLISHED' for c in conns)
        finally:
            for s in (client, accepted, server):
                s.close()


# ---------------------------------------------------------------- graph

class TestGraph:

    def test_nodes_edges_and_removal(self):
        g = graph.DiGraph()
        g.add_node('a', confidence=0.9)
        g.add_edge('a', 'b')
        g.add_edge('c', 'a')
        assert g.number_of_nodes() == 3 and g.number_of_edges() == 2
        assert list(g.successors('a')) == ['b'] and list(g.predecessors('a')) == ['c']
        assert g.nodes['a']['confidence'] == 0.9 and g.has_edge('a', 'b')
        g.remove_node('a')
        assert g.number_of_edges() == 0 and not g.has_node('a')
        assert g.edges() == []

    def test_missing_node_errors(self):
        g = graph.DiGraph()
        for call in (lambda: list(g.successors('x')), lambda: list(g.predecessors('x')),
                     lambda: g.remove_node('x')):
            with pytest.raises(graph.GraphError):
                call()


# ---------------------------------------------------------------- log

class TestLog:

    def test_size_and_retention_parsing(self):
        assert parse_size("100 MB") == 100 * 1024 ** 2
        assert parse_size("1.5 KB") == 1536
        assert parse_days("10 days") == 10
        with pytest.raises(ValueError):
            parse_size("lots")
        with pytest.raises(ValueError):
            parse_days("forever")

    def test_file_sink_levels_and_caller(self, tmp_path):
        log = Logger(name="polis-test")
        log.remove()
        sink = log.add(str(tmp_path / "run_{time}.log"), level="INFO", rotation="1 MB", retention="2 days")
        log.debug("hidden")
        log.info("visible")
        log.warning("warned")
        log.error("failed")
        log.critical("down")
        log.remove(sink)
        (path,) = tmp_path.iterdir()
        text = path.read_text(encoding="utf-8")
        assert "hidden" not in text
        for word in ("visible", "warned", "failed", "down"):
            assert word in text
        assert "test_file_sink_levels_and_caller" in text  # caller function, not the logger
        assert logging.getLogger("polis-test").handlers == []

    def test_stream_sink(self):
        log = Logger(name="polis-stream")
        log.remove()
        stream = io.StringIO()
        log.add(stream, level="DEBUG")
        log.debug("debug line")
        assert "debug line" in stream.getvalue() and "DEBUG" in stream.getvalue()
