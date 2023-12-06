#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import typing
from xml.etree.ElementTree import Element

import pytest

from Annotations2Sub import Annotation


def test_ImportError():
    m = pytest.MonkeyPatch()
    m.delattr(typing, "Literal")
    from Annotations2Sub import Annotation

    m.undo()


def test_ParseAnnotationAlpha():
    def f(x):
        for i in x:
            if i.__name__ == "ParseAnnotationAlpha":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotation, "Dummy", f)
    with pytest.raises(Exception):
        Annotation.Parse(Element(""))  # type: ignore
    m.undo()


def test_ParseAnnotationColor():
    def f(x):
        for i in x:
            if i.__name__ == "ParseAnnotationColor":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotation, "Dummy", f)
    with pytest.raises(Exception):
        Annotation.Parse(Element(""))  # type: ignore
    m.undo()


def test_MakeSureElement():
    def f(x):
        for i in x:
            if i.__name__ == "MakeSureElement":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotation, "Dummy", f)
    with pytest.raises(TypeError):
        Annotation.Parse(Element(""))  # type: ignore
    m.undo()
