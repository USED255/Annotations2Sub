#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import urllib.request

from Annotations2Sub.locale import _


def YellowText(s: str) -> str:
    return "\033[33m" + s + "\033[0m"


def RedText(s: str) -> str:
    return "\033[31m" + s + "\033[0m"


def CheckUrl(url: str = "https://google.com/", timeout: float = 3.0) -> bool:
    try:
        urllib.request.urlopen(url=url, timeout=timeout)
    except:
        return False
    return True


def AnnotationsForArchive(videoId: str) -> str:
    # 移植自 https://github.com/omarroth/invidious/blob/ea0d52c0b85c0207c1766e1dc5d1bd0778485cad/src/invidious.cr#L2835
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


def VideoForInvidiou(videoId: str, invidious_domain: str):
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
