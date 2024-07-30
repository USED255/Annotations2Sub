# -*- coding: utf-8 -*-
import os

import pytest

from Annotations2Sub.utils2 import (
    AnnotationsXmlStringToSubtitleString,
    GetAnnotationsUrl,
)
from tests import garbagePath, testCasePath


def test_GetAnnotationsUrl():
    assert (
        GetAnnotationsUrl("-8kKeUuytqA")
        == "https://archive.org/download/youtubeannotations_64/-8.tar/-8k/-8kKeUuytqA.xml"
    )


def test_GetAnnotationsUrl_ValueError():
    with pytest.raises(ValueError):
        GetAnnotationsUrl("")


def test_GetMedia():
    pass


def test_AnnotationsXmlStringToSubtitleString():
    filePath = os.path.join(testCasePath, "annotations.xml.test")
    filePath2 = os.path.join(testCasePath, "annotations.ass.test")

    with open(filePath, "r", encoding="utf-8") as f:
        string = f.read()

    with open(filePath2, "r", encoding="utf-8") as f:
        string2 = f.read()

    assert (
        AnnotationsXmlStringToSubtitleString(string, title="annotations.xml.test")
        == string2
    )


def test_AnnotationsXmlStringToSubtitleString_ValueError():
    with pytest.raises(ValueError):
        AnnotationsXmlStringToSubtitleString("")
