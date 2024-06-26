#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from Annotations2Sub.Sub import Draw, DrawCommand


def test_DrawDump():
    draws = Draw()
    draws.extend(
        [
            DrawCommand(0, 0, "m"),
            DrawCommand(100, 100, "l"),
        ]
    )

    assert str(draws) == "m 0 0 l 100 100 "
