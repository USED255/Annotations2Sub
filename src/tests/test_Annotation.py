#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree
from xml.etree.ElementTree import Element

import pytest

from Annotations2Sub import Annotations
from tests import testCasePath

filePath = os.path.join(testCasePath, "annotations.xml.test")
with open(filePath, "r", encoding="utf-8") as f:
    string = f.read()
tree = xml.etree.ElementTree.fromstring(string)


def test_ParseAnnotationAlpha_ValueError():
    def f(x):
        for i in x:
            if i.__name__ == "ParseAnnotationAlpha":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotations, "Dummy", f)
    with pytest.raises(ValueError):
        Annotations.Parse(tree)

    m.undo()


def test_ParseAnnotationColor_ValueError():
    def f(x):
        for i in x:
            if i.__name__ == "ParseAnnotationColor":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotations, "Dummy", f)
    with pytest.raises(ValueError):
        Annotations.Parse(tree)

    m.undo()


def test_Parse_ValueError():
    with pytest.raises(ValueError):
        Annotations.Parse(Element(""))
