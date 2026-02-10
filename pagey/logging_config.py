"""Application-wide logging configuration.

We want consistent logging across the whole project and sane defaults:
- INFO/DEBUG go to stdout
- WARNING/ERROR/CRITICAL go to stderr

This keeps common "normal" output separate from errors in typical CLI usage.
"""

from __future__ import annotations

import logging
import sys


class _MaxLevelFilter(logging.Filter):
    """Allow records up to (and including) `max_level`."""

    def __init__(self, max_level: int) -> None:
        super().__init__()
        self._max_level = max_level

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003 (filter)
        return record.levelno <= self._max_level


def configure_logging(level: int = logging.INFO) -> None:
    """Configure root logging once.

    Calling this multiple times is safe; it won't add duplicate handlers.
    """

    root = logging.getLogger()

    # If something already configured logging (e.g., tests), don't duplicate.
    if getattr(root, "_pagey_configured", False):
        root.setLevel(level)
        return

    root.setLevel(level)

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
