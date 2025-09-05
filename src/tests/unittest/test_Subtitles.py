# -*- coding: utf-8 -*-

from Annotations2Sub import Subtitles
from Annotations2Sub.subtitles import Draw, DrawCommand, Event, Style


def test_Style():
    assert Style()


def test_str_Style():
    assert (
        str(Style())
        == "Style: {},Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n"
    )


def test_Event():
    assert Event()


def test_str_Event():
    assert str(Event()) == "Dialogue: 0,00:00:00.00,00:00:00.00,Default,,0,0,0,,\n"


def test_Sub():
    assert Subtitles()


def test_str_Sub():
    assert (
        str(Subtitles())
        == """[Script Info]
ScriptType: v4.00+
Title: Default File

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text

"""
    )


def test_repr_Sub():
    assert repr(Subtitles()) == str(Subtitles())


def test_eq_Sub():
    assert Subtitles() == Subtitles()


def test_DrawCommand():
    assert str(DrawCommand(0, 0, "m")) == "m 0 0 "


def test_Draw():
    draws = Draw()
    draws.extend(
        [
            DrawCommand(0, 0, "m"),
            DrawCommand(100, 100, "l"),
        ]
    )

    assert str(draws) == "m 0 0 l 100 100 "
