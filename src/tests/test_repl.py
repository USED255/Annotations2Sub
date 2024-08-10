# -*- coding: utf-8 -*-

import os

import pytest

from Annotations2Sub import AnnotationsXmlFileToSubtitleFile
from tests import garbagePath, baselinePath


def test_AnnotationsXmlFileToSubtitleFile():
    filePath = os.path.join(baselinePath, "annotations.xml.test")
    filePath2 = os.path.join(garbagePath, "annotations.ass.test")

    AnnotationsXmlFileToSubtitleFile(filePath, filePath2)


def test_AnnotationsXmlFileToSubtitleFile_FileNotFoundError():
    with pytest.raises(FileNotFoundError):
        AnnotationsXmlFileToSubtitleFile("", "")
