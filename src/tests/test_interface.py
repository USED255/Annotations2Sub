# -*- coding: utf-8 -*-

from Annotations2Sub import Annotation, Subtitles
from Annotations2Sub.subtitles import Event, Style


def test_repr_Annotation():
    assert repr(Annotation()) == str(Annotation())


def test_eq_Annotation():
    assert Annotation() == Annotation()


def test_repr_Style():
    assert repr(Style()) == str(Style())


def test_eq_Style():
    assert Style() == Style()


def test_repr_Event():
    assert repr(Event()) == str(Event())


def test_eq_Event():
    assert Event() == Event()


def test_repr_Sub():
    assert repr(Subtitles()) == str(Subtitles())


def test_eq_Sub():
    assert Subtitles() == Subtitles()
