#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from Annotations2Sub.Sub import Draw, Point


def test_Draw_Dump():
    draw = Draw()
    draw.Add(Point(0, 0, "m"))
    draw.Add(Point(100, 100, "l"))
    assert draw.Dump() == "m 0 0 l 100 100 "


def test_Sub_Dump():
    pass
