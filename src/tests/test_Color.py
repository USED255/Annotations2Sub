#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pytest

from Annotations2Sub.Color import Alpha, Color


def test_Color_ValueError():
    with pytest.raises(ValueError):
        Color(256, 0, 0)
    with pytest.raises(ValueError):
        Color(0, 256, 0)
    with pytest.raises(ValueError):
        Color(0, 0, 256)


def test_Alpha_ValueError():
    with pytest.raises(ValueError):
        Alpha(256)
