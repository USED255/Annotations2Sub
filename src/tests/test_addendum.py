# -*- coding: utf-8 -*-

# Baseline 和 cli 测试未覆盖的部分

import gettext
import os
import sys

import pytest

import Annotations2Sub.__main__
from Annotations2Sub import Annotation, Subtitles
from Annotations2Sub.i18n import internationalization
from Annotations2Sub.subtitles import Event, Style
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


def test_repr_Annotation():
    assert repr(Annotation()) == str(Annotation())


def test_eq_Annotation():
    assert Annotation() == Annotation()


def test_repr_Style():
    assert repr(Style()) == str(Style())


def test_eq_Style():
    assert Style() == Style()


def test_repr_Event():
    assert repr(Event()) == str(Event())


def test_eq_Event():
    assert Event() == Event()


def test_repr_Sub():
    assert repr(Subtitles()) == str(Subtitles())


def test_eq_Sub():
    assert Subtitles() == Subtitles()


def test_Err1():
    Err1("Test")


def test_Warn1():
    Warn1("Test")


def test_main():
    with pytest.raises(SystemExit):
        Annotations2Sub.__main__.main()
