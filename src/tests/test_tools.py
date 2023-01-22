#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gettext
import os
import sys

import pytest

from Annotations2Sub.tools import MakeSureStr, RedText, YellowText, internationalization

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


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
    def a(*args, **kwargs):
        raise Exception

    m = pytest.MonkeyPatch()
    m.setattr(gettext, "translation", a)

    internationalization()
