# -*- coding: utf-8 -*-
import os

import pytest

from Annotations2Sub.cli_utils import AnnotationsXmlStringToSubtitlesString
from tests import testCasePath


def test_AnnotationsXmlStringToSubtitlesString():
    file = os.path.join(testCasePath, "annotations.xml.test")
    with open(file) as f:
        assert AnnotationsXmlStringToSubtitlesString(f.read())


def test_AnnotationsXmlStringToSubtitlesString_ValueError():
    with pytest.raises(ValueError):
        AnnotationsXmlStringToSubtitlesString("")
