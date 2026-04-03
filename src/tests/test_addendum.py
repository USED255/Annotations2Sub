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
