"""
polis.log — structured logging for ΛΕΩΝΙΔΑΣ (replaces loguru).

A thin, explicit layer over the standard `logging` module:

    from polis.log import logger
    logger.info("message")
    logger.add("logs/leonidas_{time}.log", rotation="100 MB", retention="10 days", level="INFO")

Records carry the caller's module, function and line (stacklevel), so log
lines point at the code that emitted them, not at this module.
"""

import logging
import logging.handlers
import os
import re
import sys
import time
from typing import Dict, Optional, Union

_FORMAT = "%(asctime)s.%(msecs)03d | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d - %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"
_SIZE_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(B|KB|MB|GB)\s*$", re.IGNORECASE)
_DAYS_RE = re.compile(r"^\s*(\d+)\s*days?\s*$", re.IGNORECASE)
_UNITS = {"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}


def parse_size(text: str) -> int:
    """'100 MB' -> bytes."""
    m = _SIZE_RE.match(text)
    if not m:
        raise ValueError(f"Invalid size: {text!r}")
    return int(float(m.group(1)) * _UNITS[m.group(2).upper()])


def parse_days(text: str) -> int:
    """'10 days' -> 10."""
    m = _DAYS_RE.match(text)
    if not m:
        raise ValueError(f"Invalid retention: {text!r}")
    return int(m.group(1))


class Logger:
    """loguru-style facade: logger.info(...), logger.add(sink, ...), logger.remove(id)."""

    def __init__(self, name: str = "leonidas"):
        self._log = logging.getLogger(name)
        self._log.setLevel(logging.DEBUG)
        self._log.propagate = False
        self._handlers: Dict[int, logging.Handler] = {}
        self._next_id = 0
        self.add(sys.stderr, level=os.getenv("LEONIDAS_LOG_LEVEL", "DEBUG"))

    def add(self, sink: Union[str, object], level: str = "DEBUG", rotation: Optional[str] = None,
            retention: Optional[str] = None, **_ignored) -> int:
        """
        Add a sink: a stream (sys.stderr) or a file path (``{time}`` is expanded).

        Args:
            sink: Stream or path
            level: Minimum level name
            rotation: Size-based rotation, e.g. "100 MB"
            retention: Number of rotated files kept, e.g. "10 days" keeps 10 files

        Returns:
            Handler id (for remove())
        """
        if isinstance(sink, str):
            path = sink.replace("{time}", time.strftime("%Y-%m-%d_%H-%M-%S"))
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            handler: logging.Handler = logging.handlers.RotatingFileHandler(
                path,
                maxBytes=parse_size(rotation) if rotation else 0,
                backupCount=parse_days(retention) if retention else 0,
                encoding="utf-8",
                delay=True,
            )
        else:
            handler = logging.StreamHandler(sink)
        handler.setLevel(getattr(logging, level.upper()))
        handler.setFormatter(logging.Formatter(_FORMAT, _DATEFMT))
        self._log.addHandler(handler)
        handler_id = self._next_id
        self._next_id += 1
        self._handlers[handler_id] = handler
        return handler_id

    def remove(self, handler_id: Optional[int] = None) -> None:
        """Remove one handler, or all handlers when no id is given."""
        ids = [handler_id] if handler_id is not None else list(self._handlers)
        for hid in ids:
            handler = self._handlers.pop(hid)
            self._log.removeHandler(handler)
            handler.close()

    def _emit(self, level: int, message: object) -> None:
        if self._log.isEnabledFor(level):
            self._log.log(level, message, stacklevel=3)

    def debug(self, message: object) -> None:
        self._emit(logging.DEBUG, message)

    def info(self, message: object) -> None:
        self._emit(logging.INFO, message)

    def warning(self, message: object) -> None:
        self._emit(logging.WARNING, message)

    def error(self, message: object) -> None:
        self._emit(logging.ERROR, message)

    def critical(self, message: object) -> None:
        self._emit(logging.CRITICAL, message)


logger = Logger()
