#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from Annotations2Sub.Sub import Draw, Point


def test_Draw():
    draw = Draw()
    draw.Add(Point(0, 0, "m"))
    draw.Add(Point(100, 100, "l"))
    assert draw.Dump() == "m 0 0 l 100 100 "
