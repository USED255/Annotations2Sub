# -*- coding: utf-8 -*-
"""处理应用程序的国际化和本地化。

此模块使用 `gettext` 库设置并提供翻译机制。
它尝试根据系统的区域设置加载翻译文件，并提供一个简单的 `_()` 函数，
用于在整个 Annotations2Sub 应用程序中翻译字符串。
"""

"""On n'habite pas un pays, on habite une langue. Une patrie, c'est cela et rien d'autre."""

import gettext
import locale
import os
import sys


def internationalization():
    try:
        # 配合 __main__.py
        locales = os.path.join(os.path.split(os.path.realpath(__file__))[0], "locales")

        # https://stackoverflow.com/a/8377533
        if sys.platform == "win32":
            if os.getenv("LANG") == None:
                lang, __ = locale.getdefaultlocale()
                if lang is not None:
                    os.environ["LANG"] = lang

        translate = gettext.translation(
            "Annotations2Sub",
            locales,
        )
        return translate.gettext
    except FileNotFoundError:
        print("\033[31m翻译文件加载失败\033[0m", file=sys.stderr)
        return gettext.gettext


_ = internationalization()
