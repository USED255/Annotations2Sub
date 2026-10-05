# -*- coding: utf-8 -*-

# 其他测试未覆盖的部分

import gettext
import os
import sys

import pytest

from Annotations2Sub.cli import cli_entry
from Annotations2Sub.i18n import internationalization
from Annotations2Sub.utils import Err1, Warn1


def test_internationalization_FileNotFoundError():
    def f(*args, **kwargs):
        raise FileNotFoundError

    m = pytest.MonkeyPatch()
    m.setattr(gettext, "translation", f)

    assert internationalization()

    m.undo()


def test_internationalization_win32():
    m = pytest.MonkeyPatch()
    m.setattr(sys, "platform", "win32")
    m.setattr(os, "getenv", lambda x: None)

    assert internationalization()

    m.undo()


def test_Err1():
    Err1("Test")


def test_Warn1():
    Warn1("Test")


def test_main():
    with pytest.raises(SystemExit):
        cli_entry()


def test_main_unknown_error(monkeypatch, capsys):
    # cli_entry 的兜底: 未预料到的异常应该被翻译成退出码 19
    import Annotations2Sub.cli as cli

    def boom(args=None):
        raise RuntimeError("boom")

    monkeypatch.setattr(cli, "Run", boom)

    with pytest.raises(SystemExit) as error:
        cli.cli_entry([])

    assert error.value.code == 19
    stderr = capsys.readouterr().err
    assert "RuntimeError" in stderr
    assert cli._("出现未知错误") in stderr
