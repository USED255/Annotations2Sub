# -*- coding: utf-8 -*-

import urllib.request
from urllib.error import URLError

import pytest

from Annotations2Sub import cli
from Annotations2Sub.cli import Dummy, Run


def test_Dummy():
    Dummy()


def test_Run():
    with pytest.raises(SystemExit):
        Run([])


def test_CheckNetwork():
    def f(x):
        for i in x:
            if i.__name__ == "CheckNetwork":
                i()

    def urlopenMock(url, **kwargs):
        class mock:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                return b""

        return mock()

    def urlopenURLErrorMock(*args, **kwargs):
        raise URLError("")

    def GetUrlMock(url: str):
        if (
            url
            == "https://archive.org/download/youtubeannotations_53/12.tar/123/12345678911.xml"
        ):
            return ""
        pytest.fail()

    m = pytest.MonkeyPatch()
    m.setattr(cli, "Dummy", f)
    m.setattr(cli, "GetUrl", GetUrlMock)

    m.setattr(urllib.request, "urlopen", urlopenMock)
    Run("-d 12345678911".split(" "))

    m.setattr(urllib.request, "urlopen", urlopenURLErrorMock)
    Run("-d 12345678911".split(" "))

    with pytest.raises(pytest.fail.Exception):
        GetUrlMock("")

    m.undo()
