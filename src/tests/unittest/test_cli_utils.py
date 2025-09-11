# -*- coding: utf-8 -*-
import os

import pytest

from Annotations2Sub.cli_utils import AnnotationsXmlStringToSub
from tests import testCasePath


def test_AnnotationsXmlStringToSub():
    file = os.path.join(testCasePath, "annotations.xml.test")
    with open(file) as f:
        assert AnnotationsXmlStringToSub(f.read())


def test_AnnotationsXmlStringToSub_ValueError():
    with pytest.raises(ValueError):
        AnnotationsXmlStringToSub("")
