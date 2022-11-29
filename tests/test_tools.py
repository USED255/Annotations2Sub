#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import urllib.request
from Annotations2Sub.tools import (
    AnnotationsForArchive,
    RedText,
    YellowText,
    CheckUrl,
    VideoForInvidious,
)


def test_YellowText():
    assert YellowText("Test") == "\033[33mTest\033[0m"


def test_RedText():
    assert RedText("Test") == "\033[31mTest\033[0m"


def test_AnnotationsForArchive():
    assert (
        AnnotationsForArchive("-8kKeUuytqA")
        == "https://archive.org/download/youtubeannotations_64/-8.tar/-8k/-8kKeUuytqA.xml"
    )
    with pytest.raises(ValueError):
        AnnotationsForArchive("")


def test_CheckUrl():
    def a(*args, **kwargs):
        return

    def b(*args, **kwargs):
        raise Exception

    m = pytest.MonkeyPatch()
    m.setattr(urllib.request, "urlopen", a)
    assert CheckUrl() == True
    m.setattr(urllib.request, "urlopen", b)
    assert CheckUrl() == False


def test_VideoForInvidious():
    string_pseudo_response = r'{"adaptiveFormats":[{"type":"video","bitrate":1,"url":"1"},{"type":"audio","bitrate":1,"url":"2"}]}'
    byte_pseudo_response = string_pseudo_response.encode("utf-8")

    class MockResponse:
        @staticmethod
        def read():
            return byte_pseudo_response

    def mock(*args, **kwargs):
        return MockResponse()

    m = pytest.MonkeyPatch()
    m.setattr(urllib.request, "urlopen", mock)

    return_value = VideoForInvidious("1", "2")
    expected_value = ("1", "2")
    assert return_value == expected_value
