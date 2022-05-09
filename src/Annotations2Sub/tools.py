#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import urllib.request


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
    # 参考自 https://github.com/omarroth/invidious/blob/ea0d52c0b85c0207c1766e1dc5d1bd0778485cad/src/invidious.cr#L2835
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
