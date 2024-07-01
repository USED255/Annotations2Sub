#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""工具类"""

import json
import re
import sys
import urllib.request
from typing import Any

from Annotations2Sub.i18n import _


class flags:
    def __init__(self):
        self.verbose = False


Flags = flags()


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


def GetMedia(videoId: str, instanceDomain: str):  # -> tuple[str, str]:
    url = f"https://{instanceDomain}/api/v1/videos/{videoId}"
    Stderr(_("获取 {}").format(url))
    data = json.loads(GetUrl(url))
    videos = []
    audios = []
    for i in data.get("adaptiveFormats"):
        if re.match("video", i.get("type")) != None:
            videos.append(i)
        if re.match("audio", i.get("type")) != None:
            audios.append(i)
    videos.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
    audios.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
    video = MakeSureStr(videos[0]["url"])
    audio = MakeSureStr(audios[0]["url"])
    if not video.startswith("http"):
        raise ValueError(_("没有 Video"))
    if not audio.startswith("http"):
        raise ValueError(_("没有 Audio"))
    return video, audio
