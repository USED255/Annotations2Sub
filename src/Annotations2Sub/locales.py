#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gettext
import os

locales = os.path.join(os.path.split(os.path.realpath(__file__))[0], "locales")
translate = gettext.translation(
    "Annotations2Sub",
    locales,
)
_ = translate.gettext
