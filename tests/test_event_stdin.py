"""Piped stdin event must be rejected cleanly when it is not valid UTF-8."""

import asyncio
import logging
import sys

import matrix_commander.matrix_commander as mc


class _NonUtf8Buffer:
    def read(self):
        return b"\xff\xfe\x00not-utf8"


class _NonUtf8Stdin:
    buffer = _NonUtf8Buffer()


def test_non_utf8_stdin_event_counts_error_without_traceback(monkeypatch, caplog):
    mc.gs = mc.GlobalState()
    mc.gs.log = logging.getLogger("matrix-commander-test")
    before = mc.gs.err_count
    monkeypatch.setattr(sys, "stdin", _NonUtf8Stdin())

    with caplog.at_level(logging.ERROR):
        result = asyncio.run(mc.send_event(None, ["!room:example.org"], "-"))

    assert result is None
    assert mc.gs.err_count == before + 1
