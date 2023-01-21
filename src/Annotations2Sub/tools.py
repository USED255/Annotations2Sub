#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""工具类"""

import locale
import gettext
import json
import os
import re
import sys
from typing import Any, Optional
import urllib.request


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
            Lang = os.getenv("LANG")
            if Dummy():
                Lang = Dummy()
            if Lang is None:
                os.environ["LANG"], __ = locale.getdefaultlocale()  # type: ignore

        translate = gettext.translation(
            "Annotations2Sub",
            locales,
        )
        return translate.gettext
    except:
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


def MakeSureStr(s: Optional[str]) -> str:
    """确保输入的是字符串"""

    # 这个是用来应付类型注释了, 我觉得在输入确定的环境里做类型检查没有必要
    if isinstance(s, str):
        return str(s)
    raise TypeError


def urllibWapper(url: str) -> str:
    with urllib.request.urlopen(url) as r:
        return r.read().decode("utf-8")


def DummyLiteral():
    class a:
        def __getitem__(self, b):
            return b

    return a()


def Dummy(*args, **kwargs) -> Any:
    pass


# 如果不生于中国就没有这个函数
def CheckUrl(url: str = "https://google.com/", timeout: float = 3.0) -> bool:
    """检查网络"""
    try:
        urllib.request.urlopen(url=url, timeout=timeout)
    except:
        return False
    return True


# 移植自 https://github.com/omarroth/invidious/blob/ea0d52c0b85c0207c1766e1dc5d1bd0778485cad/src/invidious.cr#L2835
# 向 https://archive.org/details/youtubeannotations 致敬
# 如果你对你的数据在意, 就不要把它们托付给他人
# Rain Shimotsuki 不仅是个打歌词的, 他更是一位创作者
# 自己作品消失, 我相信没人愿意看到
def AnnotationsForArchive(videoId: str) -> str:
    """返回注释在互联网档案馆的网址"""
    ARCHIVE_URL = "https://archive.org"
    CHARS_SAFE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

    if re.match(r"[a-zA-Z0-9_-]{11}", videoId) is None:
        raise ValueError("Invalid videoId")

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


# 致谢 https://invidious.io/
# 我更想使用 Youtube-DL, 但是 Stack Overflow 没有答案
def VideoForInvidious(videoId: str, invidious_domain: str = "") -> tuple:
    """返回一个视频流和音频流网址"""
    if invidious_domain is None:
        invidious_domain = ""
    instances = []
    if invidious_domain == "":
        instances = json.loads(urllibWapper("https://api.invidious.io/instances.json"))
        invidious_domain = instances[0][0]
    count = 0
    while True:
        # https://docs.invidious.io/api/
        url = f"https://{invidious_domain}/api/v1/videos/{videoId}"
        Stderr(_("获取 {}").format(url))
        try:
            data = json.loads(urllibWapper(url))
        except:
            if instances:
                count = count + 1
                invidious_domain = instances[count][0]
                continue
            exit(1)
        videos = []
        audios = []
        for i in data.get("adaptiveFormats"):
            if re.match("video", i.get("type")) is not None:
                videos.append(i)
            if re.match("audio", i.get("type")) is not None:
                audios.append(i)
        videos.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
        audios.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
        video = MakeSureStr(videos[0]["url"])
        audio = MakeSureStr(audios[0]["url"])
        return video, audio


_ = internationalization()
