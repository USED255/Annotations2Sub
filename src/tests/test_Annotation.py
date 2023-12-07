#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import typing
from xml.etree.ElementTree import Element

import pytest

from Annotations2Sub import Annotation


def test_ParseAnnotationAlpha_ValueError():
    def f(x):
        for i in x:
            if i.__name__ == "ParseAnnotationAlpha":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotation, "Dummy", f)
    with pytest.raises(ValueError):
        Annotation.Parse(Element(""))  # type: ignore
    m.undo()


def test_ParseAnnotationColor_ValueError():
    def f(x):
        for i in x:
            if i.__name__ == "ParseAnnotationColor":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotation, "Dummy", f)
    with pytest.raises(ValueError):
        Annotation.Parse(Element(""))  # type: ignore
    m.undo()


def test_MakeSureElement_TypeError():
    def f(x):
        for i in x:
            if i.__name__ == "MakeSureElement":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotation, "Dummy", f)
    with pytest.raises(TypeError):
        Annotation.Parse(Element(""))  # type: ignore
    m.undo()
