# -*- coding: utf-8 -*-
"""为 Annotations2Sub 应用程序提供通用实用功能。

此模块包含整个应用程序中使用的各种辅助函数，
包括用于彩色终端输出的函数（例如 `YellowText`，`RedText`），
用于错误、警告和信息消息的标准 stderr 打印函数（`Err`，`Warn`，`Info`），
以及一个简单的 URL 获取实用程序（`GetUrl`）。
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
