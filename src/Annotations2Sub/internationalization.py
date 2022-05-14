#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""On n'habite pas un pays, on habite une langue. Une patrie, c'est cela et rien d'autre."""

import gettext
import os


# 配合 __main__.py
locales = os.path.join(os.path.split(os.path.realpath(__file__))[0], "locales")

try:
    translate = gettext.translation(
        "Annotations2Sub",
        locales,
    )
    _ = translate.gettext
except:
    # 照顾 Windows
    translate = gettext.translation(
        "Annotations2Sub",
        locales,
        languages=["zh", "en"],
    )
    _ = translate.gettext
