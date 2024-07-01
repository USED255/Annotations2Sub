import os

import pytest

from Annotations2Sub import AnnotationsXmlFileToSubtitleFile
from tests import garbagePath, testCasePath

filePath = os.path.join(testCasePath, "annotations.xml.test")
filePath2 = os.path.join(garbagePath, "annotations.ass.test")


def test_AnnotationsXmlFileToSubtitleFile():
    AnnotationsXmlFileToSubtitleFile(filePath, filePath2)


def test_AnnotationsXmlFileToSubtitleFile_FileNotFoundError():
    with pytest.raises(FileNotFoundError):
        AnnotationsXmlFileToSubtitleFile("", "")
