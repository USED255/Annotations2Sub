# -*- coding: utf-8 -*-

import json
import os
import re
import xml.etree.ElementTree

from Annotations2Sub.Annotations import Parse
from Annotations2Sub.convert import Convert
from Annotations2Sub.i18n import _
from Annotations2Sub.subtitles import Subtitles
from Annotations2Sub.utils import GetUrl, Stderr, Warn


class AnnotationsStringIsEmptyError(ValueError):
    pass


def GetAnnotationsUrl(videoId: str) -> str:
    """返回注释在互联网档案馆的存档网址"""
    # 移植自 https://github.com/omarroth/invidious/blob/ea0d52c0b85c0207c1766e1dc5d1bd0778485cad/src/invidious.cr#L2835
    # 向 https://archive.org/details/youtubeannotations 致敬
    # 如果你对你的数据在意, 就不要把它们托付给他人
    # Rain Shimotsuki 不仅是个打歌词的, 他更是一位创作者
    # 自己作品消失, 我相信没人愿意看到

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
    Stderr(_('获取 "{}"').format(url))
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
    video = str(videos[0]["url"])
    audio = str(audios[0]["url"])
    if not video.startswith("http"):
        raise Exception(_("没有 Video"))
    if not audio.startswith("http"):
        raise Exception(_("没有 Audio"))
    return video, audio


def AnnotationsXmlStringToSub(
    annotations_string: str,
    transform_resolution_x: int = 100,
    transform_resolution_y: int = 100,
    font=_("Microsoft YaHei"),
    title=_("无标题"),
) -> Subtitles:

    if annotations_string == "":
        raise AnnotationsStringIsEmptyError(_("annotations_string 不应为空字符串"))

    tree = xml.etree.ElementTree.fromstring(annotations_string)
    annotations = Parse(tree)

    events = Convert(
        annotations,
        transform_resolution_x,
        transform_resolution_y,
    )

    if events == []:
        Warn(_('"{}" 没有注释被转换').format(title))

    # Annotations 是无序的
    # 按时间重新排列字幕事件, 是为了人类可读
    events.sort(key=lambda event: event.Start)

    subtitles = Subtitles()
    subtitles.comment += _("此脚本使用 Annotations2Sub 生成") + "\n"
    subtitles.comment += "https://github.com/USED255/Annotations2Sub"
    subtitles.info["Title"] = os.path.basename(title)
    subtitles.info["PlayResX"] = str(transform_resolution_x)
    subtitles.info["PlayResY"] = str(transform_resolution_y)
    subtitles.info["WrapStyle"] = "2"
    subtitles.styles["Default"].Fontname = font
    subtitles.events.extend(events)
    return subtitles
