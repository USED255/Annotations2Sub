#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gettext
import os
import sys
import urllib.request

import pytest

from Annotations2Sub.utils import (
    GetUrl,
    Internationalization,
    MakeSureStr,
    RedText,
    YellowText,
)


def test_YellowText():
    assert YellowText("Test") == "\033[33mTest\033[0m"


def test_RedText():
    assert RedText("Test") == "\033[31mTest\033[0m"


def test_MakeSureStr_TypeError():
    with pytest.raises(TypeError):
        MakeSureStr(0)  # type: ignore


def test_internationalization():
    Internationalization()


def test_internationalization_FileNotFoundError():
    def f(*args, **kwargs):
        raise FileNotFoundError

    m = pytest.MonkeyPatch()
    m.setattr(gettext, "translation", f)

    Internationalization()


def test_internationalization_win32():
    m = pytest.MonkeyPatch()
    m.setattr(sys, "platform", "win32")
    m.setattr(os, "getenv", lambda x: None)
    Internationalization()
    m.undo()


def test_GetUrl():
    def f(x):
        class mock:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                return b""

        return mock()

    m = pytest.MonkeyPatch()
    m.setattr(urllib.request, "urlopen", f)
    GetUrl("https://example.com/")
    m.undo()


def test_GetUrl_ValueError():
    with pytest.raises(ValueError):
        GetUrl("file://c:/windows/system32/drivers/config")
