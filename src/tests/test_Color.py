# -*- coding: utf-8 -*-


import pytest

from Annotations2Sub.Color import Alpha, Color, Rgba


def test_Color():
    color = Color(0, 0, 0)
    assert color.red == 0
    assert color.green == 0
    assert color.blue == 0


def test_Color_ValueError():
    with pytest.raises(ValueError):
        Color(256, 0, 0)
    with pytest.raises(ValueError):
        Color(0, 256, 0)
    with pytest.raises(ValueError):
        Color(0, 0, 256)


def test_Alpha():
    alpha = Alpha(0)
    assert alpha.alpha == 0


def test_Alpha_ValueError():
    with pytest.raises(ValueError):
        Alpha(256)


def test_Rgba():
    rgba = Rgba(Color(0, 0, 0), Alpha(0))
    assert rgba.red == 0
    assert rgba.green == 0
    assert rgba.blue == 0
    assert rgba.alpha == 0
