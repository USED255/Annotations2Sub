#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from xml.etree.ElementTree import Element

import pytest

from Annotations2Sub import Annotations


def test_ParseAnnotationAlpha_ValueError():
    def f(x):
        for i in x:
            if i.__name__ == "ParseAnnotationAlpha":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotations, "Dummy", f)
    with pytest.raises(ValueError):
        Annotations.Parse(Element(""))

    m.undo()


def test_ParseAnnotationColor_ValueError():
    def f(x):
        for i in x:
            if i.__name__ == "ParseAnnotationColor":
                i(None)

    m = pytest.MonkeyPatch()
    m.setattr(Annotations, "Dummy", f)
    with pytest.raises(ValueError):
        Annotations.Parse(Element(""))

    m.undo()
