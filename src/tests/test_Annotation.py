#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree
from xml.etree.ElementTree import Element

import pytest

from Annotations2Sub import Annotation, Annotations
from tests import testCasePath

filePath = os.path.join(testCasePath, "annotations.xml.test")
with open(filePath, "r", encoding="utf-8") as f:
    string = f.read()
tree = xml.etree.ElementTree.fromstring(string)


def test_Annotation():
    assert Annotation()


def test_str_Annotation():
    assert (
        str(Annotation())
        == "bgc=16777215,bgo=0.8,fgc=16777215,txsz=3.15,tp=text,x=0.0,y=0.0,w=0.0,h=0.0,ts=00,te=00,s=popup,t="
    )


def test_repr_Annotation():
    assert repr(Annotation()) == str(Annotation())


def test_Pares():
    assert Annotations.Parse(tree)


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
