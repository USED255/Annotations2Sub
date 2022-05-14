#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import urllib.request

from Annotations2Sub.internationalization import _


def YellowText(s: str) -> str:
    return "\033[33m" + s + "\033[0m"


def RedText(s: str) -> str:
    return "\033[31m" + s + "\033[0m"

# 如果不生于中国就没有这个函数
def CheckUrl(url: str = "https://google.com/", timeout: float = 3.0) -> bool:
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
def VideoForInvidious(videoId: str, invidious_domain: str):
    # https://docs.invidious.io/api/
    url = f"https://{invidious_domain}/api/v1/videos/{videoId}"
    print(_("获取 {}").format(url))
    string = urllib.request.urlopen(url).read().decode("utf-8")
    data = json.loads(string)
    videos = []
    audios = []
    for i in data.get("adaptiveFormats"):
        if re.match("video", i.get("type")) is not None:
            videos.append(i)
        if re.match("audio", i.get("type")) is not None:
            audios.append(i)
    videos.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
    audios.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
    return videos[0]["url"], audios[0]["url"]
