import gettext
import os
import sys

import pytest

from Annotations2Sub.i18n import Internationalization


def test_internationalization():
    Internationalization()


def test_internationalization_FileNotFoundError():
    def f(*args, **kwargs):
        raise FileNotFoundError

    m = pytest.MonkeyPatch()
    m.setattr(gettext, "translation", f)

    Internationalization()


def test_internationalization_win32():
    m = pytest.MonkeyPatch()
    m.setattr(sys, "platform", "win32")
    m.setattr(os, "getenv", lambda x: None)
    Internationalization()
    m.undo()
