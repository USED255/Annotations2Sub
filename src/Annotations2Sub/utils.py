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
        self.verbose = False


Flags = flags()


def Internationalization():
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
        Err("翻译文件加载失败")
        return gettext.gettext


def YellowText(string: str) -> str:
    """返回黄色文本"""
    return f"\033[33m{string}\033[0m"


def RedText(string: str) -> str:
    """返回红色文本"""
    return f"\033[31m{string}\033[0m"


def Stderr(string: str):
    """打印到标准错误"""
    print(string, file=sys.stderr)


def Err(string: str):
    Stderr(RedText(_("错误: ") + string))


def Warn(string: str):
    Stderr(YellowText(_("警告: ") + string))


def MakeSureStr(string: Any) -> str:
    """确保输入的是字符串"""

    # 这个是用来应付类型注释的, 我觉得在输入确定的环境里做类型检查没有必要
    if isinstance(string, str):
        return str(string)
    raise TypeError


def GetUrl(url: str) -> str:
    if not url.startswith("http"):
        raise ValueError(_('"url" 必须是 http(s)'))
    with urllib.request.urlopen(url) as r:
        return r.read().decode("utf-8")


_ = Internationalization()
