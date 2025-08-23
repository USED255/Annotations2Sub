# -*- coding: utf-8 -*-

import ssl
import sys
import urllib.request

from Annotations2Sub._flags import Flags
from Annotations2Sub.i18n import _

isatty = sys.stdout.isatty()


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
    v1 = ""
    if not isatty:
        v1 = _("错误: ")
    Stderr(RedText(v1 + string))


def Warn(string: str):
    v1 = ""
    if not isatty:
        v1 = _("警告: ")
    Stderr(YellowText(v1 + string))


def Info(string: str):
    if Flags.verbose:
        Stderr(string)


def GetUrl(url: str) -> str:
    if not url.startswith("http"):
        raise ValueError(_('"url" 必须是 http(s)'))

    context = ssl.create_default_context()
    try:
        import certifi

        context = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        if sys.platform == "win32":
            Warn(_("没有 certifi，可能会 SSL 验证失败"))

    with urllib.request.urlopen(url, context=context) as r:
        return r.read().decode("utf-8")
