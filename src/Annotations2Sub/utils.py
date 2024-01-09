#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""工具类"""

import gettext
import locale
import os
import re
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
            if os.getenv("LANG") == None:
                os.environ["LANG"], __ = locale.getdefaultlocale()  # type: ignore

        translate = gettext.translation(
            "Annotations2Sub",
            locales,
        )
        return translate.gettext
    except FileNotFoundError:
        Err("翻译文件加载失败")
        return gettext.gettext


_ = Internationalization()


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
    if isinstance(string, str):
        return str(string)
    raise TypeError(_("不是字符串"))


def GetUrl(url: str) -> str:
    if not url.startswith("http"):
        raise ValueError(_('"url" 必须是 http(s)'))
    with urllib.request.urlopen(url) as r:
        return r.read().decode("utf-8")


def GetAnnotationsUrl(videoId: str) -> str:
    # 移植自 https://github.com/omarroth/invidious/blob/ea0d52c0b85c0207c1766e1dc5d1bd0778485cad/src/invidious.cr#L2835
    # 向 https://archive.org/details/youtubeannotations 致敬
    # 如果你对你的数据在意, 就不要把它们托付给他人
    # Rain Shimotsuki 不仅是个打歌词的, 他更是一位创作者
    # 自己作品消失, 我相信没人愿意看到
    """返回注释在互联网档案馆的网址"""
    ARCHIVE_URL = "https://archive.org"
    CHARS_SAFE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

    if re.match(r"[a-zA-Z0-9_-]{11}", videoId) == None:
        raise ValueError(_("无效的 videoId"))

    index = CHARS_SAFE.index(videoId[0]).__str__().rjust(2, "0")

    # IA doesn't handle leading hyphens,
    # so we use https://archive.org/details/youtubeannotations_64
    if index == "62":
        index = "64"
        videoId.replace("^-", "A")

    file = f"{videoId[0:3]}/{videoId}.xml"

    return (
        f"{ARCHIVE_URL}/download/youtubeannotations_{index}/{videoId[0:2]}.tar/{file}"
    )
