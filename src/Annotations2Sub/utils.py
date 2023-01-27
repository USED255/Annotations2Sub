#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""工具类"""

import gettext
import locale
import os
import sys
import urllib.request
from typing import Any


class flags:
    def __init__(self):
        self.unstable = False
        self.verbose = False


Flags = flags()


def internationalization():
    """On n'habite pas un pays, on habite une langue. Une patrie, c'est cela et rien d'autre."""
    try:
        # 配合 __main__.py
        locales = os.path.join(os.path.split(os.path.realpath(__file__))[0], "locales")

        # https://stackoverflow.com/a/8377533
        if sys.platform == "win32":
            if os.getenv("LANG") is None:
                os.environ["LANG"], __ = locale.getdefaultlocale()  # type: ignore

        translate = gettext.translation(
            "Annotations2Sub",
            locales,
        )
        return translate.gettext
    except FileNotFoundError:
        Stderr(RedText("翻译文件加载失败"))
        return gettext.gettext


def YellowText(s: str) -> str:
    """返回黄色文本"""
    return "\033[33m" + s + "\033[0m"


def RedText(s: str) -> str:
    """返回红色文本"""
    return "\033[31m" + s + "\033[0m"


def Stderr(s: str):
    """打印到标准错误"""
    print(s, file=sys.stderr)


def MakeSureStr(s: Any) -> str:
    """确保输入的是字符串"""

    # 这个是用来应付类型注释了, 我觉得在输入确定的环境里做类型检查没有必要
    if isinstance(s, str):
        return str(s)
    raise TypeError


def urllibWapper(url: str) -> str:
    with urllib.request.urlopen(url) as r:
        return r.read().decode("utf-8")


_ = internationalization()
