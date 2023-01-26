#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from xml.etree.ElementTree import Element

import pytest

from Annotations2Sub import Annotation


def test_ParseAnnotationAlpha():
    def a(b):
        for i in b:
            if i.__name__ == "ParseAnnotationAlpha":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotation, "Dummy", a)
    with pytest.raises(Exception):
        Annotation.Parse(Element(""))  # type: ignore
    m.undo()


def test_ParseAnnotationColor():
    def a(b):
        for i in b:
            if i.__name__ == "ParseAnnotationColor":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotation, "Dummy", a)
    with pytest.raises(Exception):
        Annotation.Parse(Element(""))  # type: ignore
    m.undo()


def test_MakeSureElement():
    def a(b):
        for i in b:
            if i.__name__ == "MakeSureElement":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotation, "Dummy", a)
    with pytest.raises(TypeError):
        Annotation.Parse(Element(""))  # type: ignore
    m.undo()
