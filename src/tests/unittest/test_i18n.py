# -*- coding: utf-8 -*-

from Annotations2Sub.i18n import internationalization


def test_internationalization():
    assert internationalization()


def test_gettext():
    _ = internationalization()
    assert _("警告: ") == "警告: "
