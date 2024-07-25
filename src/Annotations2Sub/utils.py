#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""工具类"""


import sys
import urllib.request

from Annotations2Sub._flags import Flags
from Annotations2Sub.i18n import _


def YellowText(string: str) -> str:
    """返回黄色文本"""
    return f"\033[33m{string}\033[0m"


def RedText(string: str) -> str:
    """返回红色文本"""
    return f"\033[31m{string}\033[0m"


def Stderr(string: str):
    return
    """打印到标准错误"""
    print(string, file=sys.stderr)


def Err(string: str):
    Stderr(RedText(_("错误: ") + string))


def Warn(string: str):
    Stderr(YellowText(_("警告: ") + string))


def Info(string: str):
    if Flags.verbose:
        Stderr(string)


def GetUrl(url: str) -> str:
    if not url.startswith("http"):
        raise ValueError(_('"url" 必须是 http(s)'))
    with urllib.request.urlopen(url) as r:
        return r.read().decode("utf-8")
