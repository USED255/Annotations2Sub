#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pytest

from Annotations2Sub.Sub import Draw, DrawCommand, Sub


def test_DrawDump():
    draw = Draw()
    draw.Add(DrawCommand(0, 0, "m"))
    draw.Add(DrawCommand(100, 100, "l"))
    assert draw.Dump() == "m 0 0 l 100 100 "
    with pytest.raises(TypeError):
        draw = Draw()
        draw.Add(1)  # type: ignore


def test_str():
    subtitle = Sub()
    str(subtitle._info)
    str(subtitle._styles)
    str(subtitle._events)
    str(subtitle)

    draw = Draw()
    str(draw)
