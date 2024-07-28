# -*- coding: utf-8 -*-

from Annotations2Sub import Sub
from Annotations2Sub._Sub import Draw, DrawCommand, Event, Style


def test_Style():
    Style()


def test_Event():
    Event()


def test_Sub():
    Sub()


def test_repr_Sub():
    assert repr(Sub()) == str(Sub())


def test_DrawCommand():
    DrawCommand(0, 0, "m")


def test_Draw():
    draws = Draw()
    draws.extend(
        [
            DrawCommand(0, 0, "m"),
            DrawCommand(100, 100, "l"),
        ]
    )

    assert str(draws) == "m 0 0 l 100 100 "
