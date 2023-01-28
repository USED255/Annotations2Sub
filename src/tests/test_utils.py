#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gettext
import os

import pytest

from Annotations2Sub.utils import MakeSureStr, RedText, YellowText, internationalization


def test_YellowText():
    assert YellowText("Test") == "\033[33mTest\033[0m"


def test_RedText():
    assert RedText("Test") == "\033[31mTest\033[0m"


def test_MakeSureStr():
    with pytest.raises(TypeError):
        MakeSureStr(0)  # type: ignore


def test_internationalization():
    internationalization()


def test_internationalization2():
    def f(*args, **kwargs):
        raise FileNotFoundError

    m = pytest.MonkeyPatch()
    m.setattr(gettext, "translation", f)

    internationalization()
