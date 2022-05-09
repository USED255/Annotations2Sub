#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import os
import re
import urllib.request

from black import Any


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


def VideoForInvidiou(videoId: str, invidious_domain: str):
    api = "/api/v1/videos/"
    url = f"https://{invidious_domain}{api}{videoId}"
    string = urllib.request.urlopen(url).read().decode("utf-8")
    data = json.loads(string)
    audios = []
    videos = []
    for i in data.get("adaptiveFormats"):
        if re.match("audio", i.get("type")) is not None:
            audios.append(i)
        if re.match("video", i.get("type")) is not None:
            videos.append(i)
    audios.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
    videos.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
    return {"audios": audios, "videos": videos}


def PreviewVideo(videoId: str, file: str, invidious_domain):
    data = VideoForInvidiou(videoId, invidious_domain)
    video = data["videos"][0]
    audio = data["audios"][0]
    cmd = r'mpv "{}" --audio-file="{}" --sub-file="{}"'.format(video, audio, file)
    print(cmd)
    exit_code = os.system(cmd)
    if exit_code != 0:
        print(YellowText("exit with {}".format(exit_code)))


def GenerateVideo(videoId: str, file: str, invidious_domain: str = "invidiou.site"):
    data = VideoForInvidiou(videoId, invidious_domain)
    video = data["videos"][0]
    audio = data["audios"][0]
    cmd = r'ffmpeg -i "{}" -i "{}" -vf "ass={}" "{}.mp4"'.format(
        video, audio, file, videoId
    )
    print(cmd)
    exit_code = os.system(cmd)
    if exit_code != 0:
        print(YellowText("exit with {}".format(exit_code)))
