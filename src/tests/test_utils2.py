# -*- coding: utf-8 -*-
import os

import pytest

from Annotations2Sub import utils2
from Annotations2Sub.utils2 import (
    AnnotationsXmlStringToSubtitleString,
    GetAnnotationsUrl,
)
from tests import testCasePath


def test_GetAnnotationsUrl():
    assert (
        GetAnnotationsUrl("-8kKeUuytqA")
        == "https://archive.org/download/youtubeannotations_64/-8.tar/-8k/-8kKeUuytqA.xml"
    )


def test_GetAnnotationsUrl_ValueError():
    with pytest.raises(ValueError):
        GetAnnotationsUrl("")


def test_GetMedia():
    def GetUrlMock(url: str):
        if url == "https://good.instance/api/v1/videos/-8kKeUuytqA":
            return r'{"adaptiveFormats":[{"type":"video","bitrate":1,"url":"https://1/video"},{"type":"audio","bitrate":1,"url":"https://1/audio"}]}'

    m = pytest.MonkeyPatch()
    m.setattr(utils2, "GetUrl", GetUrlMock)

    assert utils2.GetMedia("-8kKeUuytqA", "good.instance") == (
        "https://1/video",
        "https://1/audio",
    )

    m.undo()


def test_AnnotationsXmlStringToSubtitleString():
    filePath = os.path.join(testCasePath, "annotations.xml.test")
    filePath2 = os.path.join(testCasePath, "annotations.ass.test")

    with open(filePath, "r", encoding="utf-8") as f:
        string = f.read()

    with open(filePath2, "r", encoding="utf-8") as f:
        string2 = f.read()

    assert (
        AnnotationsXmlStringToSubtitleString(
            string, 1000, 1000, "Arial", "annotations.xml.test"
        )
        == string2
    )


def test_AnnotationsXmlStringToSubtitleString_ValueError():
    with pytest.raises(ValueError):
        AnnotationsXmlStringToSubtitleString("")
