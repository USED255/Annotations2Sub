#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""On n'habite pas un pays, on habite une langue. Une patrie, c'est cela et rien d'autre."""

import gettext
import locale
import os
import sys

from Annotations2Sub.tools import Dummy

# 配合 __main__.py
locales = os.path.join(os.path.split(os.path.realpath(__file__))[0], "locales")

try:
    Dummy()
    # https://stackoverflow.com/a/8377533
    if sys.platform == "win32":
        if os.getenv("LANG") is None:
            os.environ["LANG"], enc = locale.getdefaultlocale()  # type: ignore

    translate = gettext.translation(
        "Annotations2Sub",
        locales,
    )
    _ = translate.gettext
except:
    print("翻译文件加载失败", file=sys.stderr)
    _ = gettext.gettext
