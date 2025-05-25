# -*- coding: utf-8 -*-
"""Provides common utility functions for the Annotations2Sub application.

This module contains various helper functions used across the application,
including functions for colored terminal output (e.g., `YellowText`, `RedText`),
standardized printing to stderr for errors, warnings, and informational messages
(`Err`, `Warn`, `Info`), and a simple URL fetching utility (`GetUrl`).
"""

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
