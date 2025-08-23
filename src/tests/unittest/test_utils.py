# -*- coding: utf-8 -*-


import sys
import urllib.request

import pytest

from Annotations2Sub.utils import (
    Err,
    Err1,
    Err2,
    GetUrl,
    Info,
    RedText,
    Stderr,
    Warn,
    Warn1,
    Warn2,
    YellowText,
)


def test_YellowText():
    assert YellowText("Test") == "\033[33mTest\033[0m"


def test_RedText():
    assert RedText("Test") == "\033[31mTest\033[0m"


def test_Stderr():
    Stderr("Test")


def test_Err():
    Err("Test")


def test_Warn():
    Warn("Test")


def test_Info():
    Info("Test")


def test_Err1():
    Err1("Test")


def test_Warn1():
    Warn1("Test")


def test_Err2():
    Err2("Test")


def test_Warn2():
    Warn2("Test")


def test_GetUrl():
    def f(*args, **kwargs):
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


def test_GetUrl_no_certifi():
    def f(*args, **kwargs):
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
    m.setitem(sys.modules, "certifi", None)

    GetUrl("https://example.com/")

    m.undo()


def test_GetUrl_ValueError():
    with pytest.raises(ValueError):
        GetUrl("file://c:/windows/system32/drivers/config")
