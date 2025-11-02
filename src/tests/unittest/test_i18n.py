# -*- coding: utf-8 -*-

import gettext
import os
import sys

import pytest

from Annotations2Sub.i18n import internationalization


def test_internationalization():
    assert internationalization()


def test_internationalization_FileNotFoundError():
    def f(*args, **kwargs):
        raise FileNotFoundError

    m = pytest.MonkeyPatch()
    m.setattr(gettext, "translation", f)

    assert internationalization()

    m.undo()


def test_internationalization_win32():
    m = pytest.MonkeyPatch()
    m.setattr(sys, "platform", "win32")
    m.setattr(os, "getenv", lambda x: None)

    assert internationalization()

    m.undo()


def test_gettext():
    _ = internationalization()
    assert _("警告: ") == "警告: "
