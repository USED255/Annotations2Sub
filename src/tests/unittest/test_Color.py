# -*- coding: utf-8 -*-

import pytest

from Annotations2Sub.color import Alpha, Color, Rgba


def test_Color():
    color = Color(0, 0, 0)
    assert color.red == 0
    assert color.green == 0
    assert color.blue == 0


def test_Alpha():
    alpha = Alpha(0)
    assert alpha.alpha == 0


def test_Rgba():
    rgba = Rgba(Color(0, 0, 0), Alpha(0))
    assert rgba.red == 0
    assert rgba.green == 0
    assert rgba.blue == 0
    assert rgba.alpha == 0
