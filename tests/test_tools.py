#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request

import pytest
from Annotations2Sub import tools

from Annotations2Sub.tools import (
    AnnotationsForArchive,
    CheckUrl,
    RedText,
    VideoForInvidious,
    YellowText,
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

    def mock(*args, **kwargs):
        return string_pseudo_response

    m = pytest.MonkeyPatch()
    m.setattr(tools, "urllibWapper", mock)

    return_value = VideoForInvidious("1", "2")
    expected_value = ("1", "2")
    assert return_value == expected_value
