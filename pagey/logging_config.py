"""Application-wide logging configuration.

We want consistent logging across the whole project and sane defaults:
- INFO/DEBUG go to stdout
- WARNING/ERROR/CRITICAL go to stderr

This keeps common "normal" output separate from errors in typical CLI usage.

Environment variables:
- PAGEY_LOG_LEVEL: DEBUG|INFO|WARNING|ERROR|CRITICAL (default: INFO)
"""

from __future__ import annotations

import logging
import os
import sys


class _MaxLevelFilter(logging.Filter):
    """Allow records up to (and including) `max_level`."""

    def __init__(self, max_level: int) -> None:
        super().__init__()
        self._max_level = max_level

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003 (filter)
        return record.levelno <= self._max_level


def _parse_level(level: str | int | None) -> int:
    if level is None:
        return logging.INFO
    if isinstance(level, int):
        return level

    normalized = level.strip().upper()

    # Accept numeric values too
    if normalized.isdigit():
        return int(normalized)

    mapping = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "NOTSET": logging.NOTSET,
    }
    return mapping.get(normalized, logging.INFO)


def configure_logging(level: str | int | None = None) -> None:
    """Configure root logging once.

    Calling this multiple times is safe; it won't add duplicate handlers.
    """
    resolved_level = _parse_level(level if level is not None else os.getenv("PAGEY_LOG_LEVEL"))

    root = logging.getLogger()

    # If something already configured logging (e.g., tests), don't duplicate.
    if getattr(root, "_pagey_configured", False):
        root.setLevel(resolved_level)
        return

    root.setLevel(resolved_level)

    fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    # stdout handler for <= INFO
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(_MaxLevelFilter(logging.INFO))
    stdout_handler.setFormatter(formatter)

    # stderr handler for >= WARNING
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(formatter)

    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)

    setattr(root, "_pagey_configured", True)
