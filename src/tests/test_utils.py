#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gettext
import os

import pytest

from Annotations2Sub.utils import (
    MakeSureStr,
    RedText,
    YellowText,
    internationalization,
    urllibWapper,
)

basePath = os.path.dirname(__file__)
file1 = os.path.join(basePath, "test", "1.test")


def test_YellowText():
    assert YellowText("Test") == "\033[33mTest\033[0m"


def test_RedText():
    assert RedText("Test") == "\033[31mTest\033[0m"


def test_MakeSureStr():
    with pytest.raises(TypeError):
        MakeSureStr(0)  # type: ignore


def test_internationalization():
    internationalization()


def test_internationalization2():
    def a(*args, **kwargs):
        raise Exception

    m = pytest.MonkeyPatch()
    m.setattr(gettext, "translation", a)

    internationalization()


def test_urllibWapper():
    def a():
        import http.server
        import socketserver

        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", 10575), Handler) as httpd:
            httpd.serve_forever()

    import _thread

    _thread.start_new_thread(a, ())
    urllibWapper("http://127.0.0.1:10575/")
