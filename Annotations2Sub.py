#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Annotations2Sub
__authors__ = "wrtyis@outlook.com"
__license__ = "GPLv3"
__version__ = "0.0.8"
"""
参考:
https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
https://github.com/afrmtbl/AnnotationsRestored
https://github.com/iv-org/invidious

"""
""" 
鸣谢:
https://archive.org/details/youtubeannotations
"""
""" 
本脚本启发自:
https://github.com/nirbheek/youtube-ass 您仍然可以从本脚本找到他的痕迹。

"""

import os

if hex(os.sys.hexversion) < hex(0x03060000):
    print("This script does not work on Python versions lower than 3.6")
    exit(1)
import re
import json
import glob
import urllib.request
import urllib.error
import gettext
import argparse
import traceback
import threading
import xml.etree.ElementTree
from datetime import datetime
from typing import Optional, Union

_ = gettext.gettext

# 应该用无衬线字体,但是好像不能方便的使用字体家族..
font = "Microsoft YaHei UI"


def _normal_text(s: str) -> str:
    return s


def _yellow_text(s: str) -> str:
    return "\033[0;33;40m{}\033[0m".format(s)


def _red_text(s: str) -> str:
    return "\031[0;31;40m{}\031[0m".format(s)


def PriI(s, *args: object) -> None:
    _text = _normal_text
    if args == ():
        print(_text(_(s)))
        return
    print(_text(_(s).format(*args)))


def PriW(s, *args: object) -> None:
    _text = _yellow_text
    if args == ():
        print(_text(_(s)))
        return
    print(_text(_(s).format(*args)))


def PriW(s, *args: object) -> None:
    _text = _yellow_text
    if args == ():
        print(_text(_(s)))
        return
    print(_text(_(s).format(*args)))


def PriE(s, *args: object) -> None:
    _text = _red_text
    if args == ():
        print(_text(_(s)))
        return
    print(_text(_(s).format(*args)))


def _check_url(url: str = "https://google.com/", timeout: float = 3.0) -> bool:
    try:
        urllib.request.urlopen(url=url, timeout=timeout)
    except:
        return False
    return True


def _check_network():
    if _check_url() is not True:
        PriW("您好像无法访问Google🤔")


def check_network():
    check_thread = threading.Thread(target=_check_network)
    check_thread.start()


def download_annotations_for_archive(video_id: str) -> str:
    # 参考自 https://github.com/omarroth/invidious/blob/ea0d52c0b85c0207c1766e1dc5d1bd0778485cad/src/invidious.cr#L2835
    ARCHIVE_URL = r"https://archive.org"
    CHARS_SAFE = r"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

    m = re.match(r"[a-zA-Z0-9_-]{11}", video_id)
    if m != None:
        videoId = m.group()
    index = CHARS_SAFE.index(videoId[0]).__str__().rjust(2, "0")

    if index == "62":
        index = "64"
        videoId.replace(r"^-", "A")
    file = r"{}/{}.xml".format(videoId[0:3], videoId)
    url = ARCHIVE_URL + "/download/youtubeannotations_{}/{}.tar/{}".format(
        index, videoId[0:2], file
    )

    PriI("正在从 {} 下载注释文件", url)
    annotations = urllib.request.urlopen(url).read().decode("utf-8")
    if annotations == "":
        return
    save_file = "{}.xml".format(video_id)
    with open(save_file, "w", encoding="utf-8") as f:
        f.write(annotations)
    PriI("下载完成")
    return save_file


def _get_video_for_youtube(video_id: str) -> list:
    url = "https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"

    req = urllib.request.Request(url)

    req.add_header("authority", "www.youtube.com")
    req.add_header(
        "sec-ch-ua", '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"'
    )
    req.add_header("x-origin", "https://www.youtube.com")
    req.add_header("sec-ch-ua-mobile", "?0")
    req.add_header("content-type", "application/json")
    req.add_header(
        "user-agent",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    )
    req.add_header("x-youtube-client-name", "56")
    req.add_header("x-youtube-client-version", "1.20220125.01.00")
    req.add_header("x-goog-authuser", "0")
    req.add_header("sec-ch-ua-platform", '"Windows"')
    req.add_header("accept", "*/*")
    req.add_header("origin", "https://www.youtube.com")
    req.add_header("sec-fetch-site", "same-origin")
    req.add_header("sec-fetch-mode", "cors")
    req.add_header("sec-fetch-dest", "empty")
    req.add_header("accept-language", "en")

    body_s = r"""{
        "videoId": "M7lc1UVf-VE",
        "context": {
            "client": {
                "deviceMake": "",
                "deviceModel": "",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36,gzip(gfe)",
                "clientName": "WEB_EMBEDDED_PLAYER",
                "clientVersion": "1.20220125.01.00",
                "osName": "Windows",
                "osVersion": "10.0",
                "platform": "DESKTOP",
                "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                "browserName": "Chrome",
                "browserVersion": "97.0.4692.99",
                "screenWidthPoints": 720,
                "screenHeightPoints": 406,
                "screenPixelDensity": 1,
                "screenDensityFloat": 1.25,
                "utcOffsetMinutes": 480,
                "userInterfaceTheme": "USER_INTERFACE_THEME_LIGHT",
                "connectionType": "CONN_CELLULAR_4G",
                "timeZone": "UTC",
                "playerType": "UNIPLAYER",
                "tvAppInfo": {
                    "livingRoomAppMode": "LIVING_ROOM_APP_MODE_UNSPECIFIED"
                },
                "clientScreen": "EMBED"
            },
            "request": {
                "useSsl": true,
                "internalExperimentFlags": [],
                "consistencyTokenJars": []
            }
        }
    }"""

    body = json.loads(body_s)
    body["videoId"] = video_id

    res = json.loads(
        urllib.request.urlopen(req, data=json.dumps(body).encode("utf-8"))
        .read()
        .decode("utf-8")
    )
    try:
        if res["playabilityStatus"]["reason"] == "Video unavailable":
            PriE("Video unavailable")
            exit(0)
    except:
        pass
    return res["streamingData"]["adaptiveFormats"]


def _get_video(video_id: str):
    data = _get_video_for_youtube(video_id)
    audios = []
    videos = []
    for i in data:
        if re.match("audio", i.get("mimeType")) is not None:
            audios.append(i)
        if re.match("video", i.get("mimeType")) is not None:
            videos.append(i)
    audios.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
    videos.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
    audio = audios[0].get("url")
    video = videos[0].get("url")
    return {"audio": audio, "video": video}


def preview_video(video_id: str, file: str) -> None:
    audio, video = _get_video(video_id).values()
    cmd = r'mpv "{}" --audio-file="{}" --sub-file="{}"'.format(video, audio, file)
    PriI(cmd)
    exit_code = os.system(cmd)
    if exit_code != 0:
        PriW("exit with {}", exit_code)


def generate_video(
    video_id: str,
    file: str,
) -> None:
    audio, video = _get_video(video_id).values()
    cmd = r'ffmpeg -i "{}" -i "{}" -vf "ass={}" "{}.mp4"'.format(
        video, audio, file, video_id
    )
    PriI(cmd)
    exit_code = os.system(cmd)
    if exit_code != 0:
        PriW("exit with {}", exit_code)


class ConvertParameterStructure:
    def __init__(self) -> None:
        self.title: str = _("默认文件")
        self.resolution_x: int = 100
        self.resolution_y: int = 100
        self.font = font
        self.libass_hack: bool = False


class Sub:
    def __init__(self) -> None:
        self.info = self._info()
        self.style = self._style()
        self.event = self._event()

    def dump(self) -> str:
        data = ""
        data += self.info.dump()
        data += self.style.dump()
        data += self.event.dump()
        return data

    class _info(object):
        def __init__(self) -> None:
            self.HEAD = "[Script Info]\n"
            self.note = (
                "; Script generated by Annotations2Sub\n"
                "; https://github.com/WRTYis/Annotations2Sub\n"
            )
            self.data = {"Title": "Default File", "ScriptType": "v4.00+"}

        def add(self, k: str, v: str) -> None:
            self.data[k] = v

        def dump(self) -> str:
            data = ""
            data += self.HEAD
            data += self.note
            for k, v in self.data.items():
                data += str(k) + ": " + str(v) + "\n"
            data += "\n"
            return data

    class _style(object):
        def __init__(self) -> None:
            self.HEAD = (
                "[V4+ Styles]\n"
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            )
            self.data = {}
            self.add(Name="Default")

        def add(
            self,
            Name: str,
            Fontname: str = "Arial",
            Fontsize: str = 20,
            PrimaryColour: str = "&H00FFFFFF",
            SecondaryColour: str = "&H000000FF",
            OutlineColour: str = "&H00000000",
            BackColour: str = "&H00000000",
            Bold: int = 0,
            Italic: int = 0,
            Underline: int = 0,
            StrikeOut: int = 0,
            ScaleX: int = 100,
            ScaleY: int = 100,
            Spacing: int = 0,
            Angle: int = 0,
            BorderStyle: int = 1,
            Outline: int = 2,
            Shadow: int = 2,
            Alignment: int = 2,
            MarginL: int = 10,
            MarginR: int = 10,
            MarginV: int = 10,
            Encoding: int = 1,
        ) -> None:
            self.data[Name] = [
                Fontname,
                Fontsize,
                PrimaryColour,
                SecondaryColour,
                OutlineColour,
                BackColour,
                Bold,
                Italic,
                Underline,
                StrikeOut,
                ScaleX,
                ScaleY,
                Spacing,
                Angle,
                BorderStyle,
                Outline,
                Shadow,
                Alignment,
                MarginL,
                MarginR,
                MarginV,
                Encoding,
            ]

        def change(
            self,
            Name,
            Fontname: Optional[str] = None,
            Fontsize: Optional[str] = None,
            PrimaryColour: Optional[str] = None,
            SecondaryColour: Optional[str] = None,
            OutlineColour: Optional[str] = None,
            BackColour: Optional[str] = None,
            Bold: Optional[int] = None,
            Italic: Optional[int] = None,
            Underline: Optional[int] = None,
            StrikeOut: Optional[int] = None,
            ScaleX: Optional[int] = None,
            ScaleY: Optional[int] = None,
            Spacing: Optional[int] = None,
            Angle: Optional[int] = None,
            BorderStyle: Optional[int] = None,
            Outline: Optional[int] = None,
            Shadow: Optional[int] = None,
            Alignment: Optional[int] = None,
            MarginL: Optional[int] = None,
            MarginR: Optional[int] = None,
            MarginV: Optional[int] = None,
            Encoding: Optional[int] = None,
        ) -> None:
            for i, v in enumerate(
                [
                    Fontname,
                    Fontsize,
                    PrimaryColour,
                    SecondaryColour,
                    OutlineColour,
                    BackColour,
                    Bold,
                    Italic,
                    Underline,
                    StrikeOut,
                    ScaleX,
                    ScaleY,
                    Spacing,
                    Angle,
                    BorderStyle,
                    Outline,
                    Shadow,
                    Alignment,
                    MarginL,
                    MarginR,
                    MarginV,
                    Encoding,
                ]
            ):
                if v is not None:
                    self.data[Name][i] = v

        def dump(self) -> str:
            data = ""
            data += self.HEAD
            for Name, Style in self.data.items():
                data += "Style: {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                    Name, *Style
                )
            data += "\n"
            return data

    class _event(object):
        def __init__(self) -> None:
            self.HEAD = (
                "[Events]\n"
                "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
            )
            self.data = []

        def add(
            self,
            EventType: str = "Dialogue",
            Layer: int = 0,
            Start: str = "0:00:00.00",
            End: str = "0:00:00.00",
            Style: str = "Default",
            Name: str = "",
            MarginL: int = 0,
            MarginR: int = 0,
            MarginV: int = 0,
            Effect: str = "",
            Text: str = "",
        ) -> None:
            # EventType: Dialogue, Comment, Picture, Sound, Movie, Command
            self.data.append(
                [
                    EventType,
                    Layer,
                    Start,
                    End,
                    Style,
                    Name,
                    MarginL,
                    MarginR,
                    MarginV,
                    Effect,
                    Text,
                ]
            )

        def dump(self) -> str:
            data = ""
            data += self.HEAD
            for event in self.data:
                data += "{}: {},{},{},{},{},{},{},{},{},{}\n".format(*event)
            data += "\n"
            return data


def TabHelper(
    Text: str = "",
    PrimaryColour: Optional[str] = None,
    SecondaryColour: Optional[str] = None,
    BorderColor: Optional[str] = None,
    ShadowColor: Optional[str] = None,
    PosX: Optional[float] = None,
    PosY: Optional[float] = None,
    fontsize: Optional[str] = None,
    PrimaryAlpha: Optional[str] = None,
    SecondaryAlpha: Optional[str] = None,
    BorderAlpha: Optional[str] = None,
    ShadowAlpha: Optional[str] = None,
    p: Optional[str] = None,
) -> str:
    _tab = ""
    if (PosX, PosY) is not None:
        _an = r"\an7"
        _pos = "\\pos({},{})".format(PosX, PosY)
        _tab += _an + _pos
    if PrimaryColour is not None:
        _c = r"\c" + PrimaryColour
        _tab += _c
    if SecondaryColour is not None:
        _2c = r"\2c" + SecondaryColour
        _tab += _2c
    if BorderColor is not None:
        _3c = r"\3c" + BorderColor
        _tab += _3c
    if ShadowColor is not None:
        _4c = r"\4c" + ShadowColor
        _tab += _4c
    if fontsize is not None:
        _fs = r"\fs" + fontsize
        _tab += _fs
    if PrimaryAlpha is not None:
        _1a = r"\1a" + PrimaryAlpha
        _tab += _1a
    if SecondaryAlpha is not None:
        _2a = r"\2a" + SecondaryAlpha
        _tab += _2a
    if BorderAlpha is not None:
        _3a = r"\3a" + BorderAlpha
        _tab += _3a
    if ShadowAlpha is not None:
        _4a = r"\4a" + ShadowAlpha
        _tab += _4a
    _text = r"{" + _tab + r"}" + Text
    return _text
    # {\2c&H2425DA&\pos(208,148)}test


class DrawHelper:
    def __init__(self) -> None:
        self.d = "m 0 0 l"

    def add_point(self, x: Union[int, float], y: Union[int, float]) -> None:
        self.d += " {} {} l".format(x, y)

    def dump(self) -> str:
        return self.d


def Convert(string: str, convert_parameter: ConvertParameterStructure) -> Sub:
    title = convert_parameter.title
    resolution_x = convert_parameter.resolution_x
    resolution_y = convert_parameter.resolution_y
    font = convert_parameter.font
    libass_hack = convert_parameter.libass_hack
    sub = Sub()
    sub.info.add(k="Title", v=title)
    sub.info.add(k="PlayResX", v=resolution_x)
    sub.info.add(k="PlayResY", v=resolution_y)
    if resolution_x != 100 or resolution_y != 100:
        libass_hack = False
    sub.style.change(Name="Default", Fontname=font)
    if libass_hack is True:
        sub.info.note += "; libass_hack=True\n"
    tree = xml.etree.ElementTree.fromstring(string)
    for each in tree.find("annotations").findall("annotation"):

        # 提取 annotation id
        Name = each.get("id")

        # 提取时间
        # h:mm:ss.ms
        _Segment = each.find("segment").find("movingRegion").findall("rectRegion")
        if len(_Segment) == 0:
            _Segment = (
                each.find("segment").find("movingRegion").findall("anchoredRegion")
            )
        if len(_Segment) == 0:
            Start = "0:00:00.00"
            End = "0:00:00.00"
        if len(_Segment) != 0:
            Start = min(_Segment[0].get("t"), _Segment[1].get("t"))
            End = max(_Segment[0].get("t"), _Segment[1].get("t"))
        if not "never" in (Start, End):
            try:
                Start = datetime.strftime(
                    datetime.strptime(Start, "%H:%M:%S.%f"), "%H:%M:%S.%f"
                )[:-4]
                End = datetime.strftime(
                    datetime.strptime(End, "%H:%M:%S.%f"), "%H:%M:%S.%f"
                )[:-4]
            except:
                Start = datetime.strftime(
                    datetime.strptime(Start, "%M:%S.%f"), "%H:%M:%S.%f"
                )[:-4]
                End = datetime.strftime(
                    datetime.strptime(End, "%M:%S.%f"), "%H:%M:%S.%f"
                )[:-4]
        if "never" in (Start, End):
            Start = "0:00:00.00"
            End = "999:00:00.00"
        # 提取样式
        style = each.get("style")

        # 提取文本
        Text = each.find("TEXT")
        if Text is not None:
            Text = Text.text
        else:
            Text = ""
        Text = Text.replace("\n", r"\N")
        TextB = Text
        TextB = TextB.replace(r"{", r"\{")
        TextB = TextB.replace(r"}", r"\}")
        if Text != TextB:
            if libass_hack == False:
                PriW("警告, 花括号转义只能在libass上工作!({})", Name)
            Text = TextB

        def _bgr2rgb(BGR: str) -> str:
            B = BGR[0:2]
            G = BGR[2:4]
            R = BGR[4:6]
            RGB = R + G + B
            return RGB

        def _convert_color(s0: str) -> str:
            # return r'&H'+_bgr2rgb(str(hex(int(s))).replace('0x','').zfill(6).upper())+r'&'
            if s0 == None:
                return
            s1 = int(s0)
            s2 = hex(s1)
            s3 = str(s2)
            s4 = s3.replace("0x", "").zfill(6).upper()
            s5 = _bgr2rgb(s4)
            s6 = r"&H{}&".format(s5)
            return s6

        def _convert_alpha(s0: str) -> str:
            # return r'&H'+str(hex(int((1-float(s))*255))).replace('0x','')+r'&'
            if s0 == None:
                return
            s1 = float(s0)
            s2 = 1 - s1
            s3 = s2 * 255
            s4 = int(s3)
            s5 = hex(s4)
            s6 = str(s5)
            s7 = s6.replace("0x", "").upper()
            s8 = r"&H{}&".format(s7)
            return s8

        _Appearance = each.find("appearance")

        if _Appearance is not None:
            fontsize = _Appearance.get("textSize")
            bgAlpha = _convert_alpha(_Appearance.get("bgAlpha"))
            fgColor = _convert_color(_Appearance.get("fgColor"))
            bgColor = _convert_color(_Appearance.get("bgColor"))
        if fgColor is None:
            fgColor = r"&H000000&"
        if bgColor is None:
            bgColor = r"&HFFFFFF&"
        if bgAlpha is None:
            bgAlpha = r"&HCC&"
        if fontsize is None:
            fontsize = 3.15
        """
            x,y: 文本框左上角的坐标
            w,h: 文本框的宽度和高度
        """
        (x, y, w, h) = map(float, (_Segment[0].get(i) for i in ("x", "y", "w", "h")))
        w = round(w, 3)
        h = round(h, 3)
        fontsize = float(fontsize) * resolution_y / 100
        x = x * resolution_x / 100
        y = y * resolution_y / 100
        w = w * resolution_x / 100
        h = h * resolution_y / 100
        FullyTransparent = r"&HFF&"

        # 按样式生成代码
        if style == "popup":
            Name += r"_popup"
            # vsfilter与libass行为不一致
            if libass_hack == True:
                w = str(round(float(w) * 1.776, 3))
            TextBox = "m 0 0 l {0} 0 l {0} {1} l 0 {1} ".format(w, h)
            TextBox = r"{\p1}" + TextBox + r"{\p0}"
            TextBox = TabHelper(
                Text=TextBox,
                PrimaryColour=bgColor,
                PosX=x,
                PosY=y,
                fontsize=str(round(float(fontsize), 3)),
                PrimaryAlpha=bgAlpha,
                SecondaryAlpha=FullyTransparent,
                BorderAlpha=FullyTransparent,
                ShadowAlpha=FullyTransparent,
            )
            sub.event.add(Start=Start, End=End, Name=Name + r"_TextBox", Text=TextBox)
            Text = TabHelper(
                Text=Text,
                PrimaryColour=fgColor,
                PosX=x + 1,
                PosY=y + 1,
                fontsize=str(round(float(fontsize), 3)),
                SecondaryAlpha=FullyTransparent,
                BorderAlpha=FullyTransparent,
                ShadowAlpha=FullyTransparent,
            )
            sub.event.add(Start=Start, End=End, Name=Name, Text=Text)
        elif style == "title":
            Name += r"_title"
            # 除以4,要不然大得离谱
            fontsize = str(round(float(fontsize) / 4, 3))
            Text = TabHelper(
                Text=Text,
                PrimaryColour=fgColor,
                PosX=x,
                PosY=y,
                fontsize=fontsize,
                SecondaryAlpha=FullyTransparent,
                BorderAlpha=FullyTransparent,
                ShadowAlpha=FullyTransparent,
            )
            sub.event.add(Start=Start, End=End, Name=Name, Text=Text)
        elif style == "speech":
            # 太难了
            PriI("抱歉这个脚本还不能支持 {} 样式. ({})", style, Name)
            Name += r"_speech_NOTSUPPORT"
            if libass_hack == True:
                w = round(float(w) * 1.776, 3)
            # 气泡锚点x
            sx = float(_Segment[0].get("sx"))
            # 气泡锚点y
            sy = float(_Segment[0].get("sy"))
            # 文本框左上角x
            x = float(x)
            # 文本框左上角y
            y = float(y)
            # 文本框右下角x
            tx = x + w
            # 文本框右下角y
            ty = y + h
            # 锚点x控制点w
            bubble_anchor_x = round(sx - x, 3)
            # 锚点y控制点h
            bubble_anchor_y = round(sy - y, 3)

            # .
            class _speech_helper:
                def __init__(
                    self, d: DrawHelper, w, h, bubble_anchor_x, bubble_anchor_y
                ) -> None:
                    self.d = d
                    self.w = w
                    self.h = h
                    self.bubble_anchor_x = bubble_anchor_x
                    self.bubble_anchor_y = bubble_anchor_y

                def 右上角(self):
                    self.d.add_point(self.w, 0)

                def 右下角(self):
                    self.d.add_point(self.w, self.h)

                def 左下角(self):
                    self.d.add_point(0, self.h)

                def 气泡锚点(self):
                    self.d.add_point(self.bubble_anchor_x, self.bubble_anchor_y)

            # ..
            if sx > x + w / 2:
                # 开口
                bubble_open_x = round(w / 2 - w * 0.2, 3)
                # 入口
                bubble_close_x = round(w / 2 - w * 0.4, 3)
            else:
                bubble_open_x = round(w / 2 - w * 0.8, 3)
                bubble_close_x = round(w / 2 - w * 0.6, 3)
            if sy > x + h / 2:
                # 开口
                bubble_open_y = round(h / 2 - h * 0.2, 3)
                # 入口
                bubble_close_y = round(h / 2 - h * 0.4, 3)
            else:
                bubble_open_y = round(h / 2 - h * 0.8, 3)
                bubble_close_y = round(h / 2 - h * 0.6, 3)
            # 锚点在气泡下方
            if sy > ty:
                d = DrawHelper()
                s = _speech_helper(d, w, h, bubble_anchor_x, bubble_anchor_y)
                #
                s.右上角()
                #
                s.右下角()
                # 气泡开口
                d.add_point(bubble_open_x, h)
                #
                s.气泡锚点()
                # 气泡闭口
                d.add_point(bubble_close_x, h)
                #
                s.左下角()
                TextBox = d.dump()
            # 锚点在气泡上方
            elif sy < y:
                d = DrawHelper()
                s = _speech_helper(d, w, h, bubble_anchor_x, bubble_anchor_y)
                # 气泡开口
                d.add_point(bubble_open_x, 0)
                #
                s.气泡锚点()
                # 气泡闭口
                d.add_point(bubble_close_x, 0)
                #
                s.右上角()
                #
                s.右下角()
                #
                s.左下角()
                TextBox = d.dump()
            # 左
            elif sy > y and sx > x + w / 2:
                d = DrawHelper()
                s = _speech_helper(d, w, h, bubble_anchor_x, bubble_anchor_y)
                #
                s.右上角()
                #
                s.右下角()
                #
                s.左下角()
                # 气泡开口
                d.add_point(0, bubble_open_y)
                #
                s.气泡锚点()
                # 气泡闭口
                d.add_point(0, bubble_close_y)
                TextBox = d.dump()
            # 右
            elif sy > y and sx < x + w / 2:
                d = DrawHelper()
                s = _speech_helper(d, w, h, bubble_anchor_x, bubble_anchor_y)
                #
                s.右上角()
                # 气泡开口
                d.add_point(w, bubble_open_y)
                #
                s.气泡锚点()
                # 气泡闭口
                d.add_point(w, bubble_close_y)
                #
                s.右下角()
                #
                s.左下角()
                TextBox = d.dump()
            else:
                PriW("? ({})", Name)
            TextBox = r"{\p1}" + TextBox + r"{\p0}"
            TextBox = TabHelper(
                Text=TextBox,
                PrimaryColour=bgColor,
                PosX=x,
                PosY=y,
                fontsize=str(round(float(fontsize), 3)),
                PrimaryAlpha=bgAlpha,
                SecondaryAlpha=FullyTransparent,
                BorderAlpha=FullyTransparent,
                ShadowAlpha=FullyTransparent,
            )
            sub.event.add(Start=Start, End=End, Name=Name + r"_TextBox", Text=TextBox)
            Text = TabHelper(
                Text=Text,
                PrimaryColour=fgColor,
                PosX=x + 1,
                PosY=y + 1,
                fontsize=str(round(float(fontsize), 3)),
                SecondaryAlpha=FullyTransparent,
                BorderAlpha=FullyTransparent,
                ShadowAlpha=FullyTransparent,
            )
            sub.event.add(Start=Start, End=End, Name=Name, Text=Text)
        elif style == "highlightText":
            # 我需要样本
            PriI("抱歉这个脚本还不能支持 {} 样式. ({})", style, Name)
            Name += r"_highlightText_NOTSUPPORT"
            if libass_hack == True:
                w = round(float(w) * 1.776, 3)
            TextBox = "m 0 0 l {0} 0 l {0} {1} l 0 {1} ".format(w, h)
            TextBox = r"{\p1}" + TextBox + r"{\p0}"
            TextBox = TabHelper(
                Text=TextBox,
                PrimaryColour=bgColor,
                PosX=x,
                PosY=y,
                fontsize=str(round(float(fontsize), 3)),
                PrimaryAlpha=bgAlpha,
                SecondaryAlpha=FullyTransparent,
                BorderAlpha=FullyTransparent,
                ShadowAlpha=FullyTransparent,
            )
            sub.event.add(Start=Start, End=End, Name=Name + r"_TextBox", Text=TextBox)
            Text = TabHelper(
                Text=Text,
                PrimaryColour=fgColor,
                PosX=x + 1,
                PosY=y + 1,
                fontsize=str(round(float(fontsize), 3)),
                SecondaryAlpha=FullyTransparent,
                BorderAlpha=FullyTransparent,
                ShadowAlpha=FullyTransparent,
            )
            sub.event.add(Start=Start, End=End, Name=Name, Text=Text)
        elif style == None:
            pass
        else:
            PriI("抱歉这个脚本还不能支持 {} 样式. ({})", style, Name)
    sub.event.data.sort(key=lambda x: x[2])
    if len(sub.event.data) == 0:
        PriW("警告, 没有注释被转换!")
    return sub


class Annotations2Sub:
    def __init__(self, file: str, convert_parameter: ConvertParameterStructure) -> None:
        string = open(file, "r", encoding="utf-8").read()
        try:
            self.sub = Convert(string=string, convert_parameter=convert_parameter)
        except xml.etree.ElementTree.ParseError:
            traceback.print_exc()
            PriW("也许选错文件了?")

    def Save(self, file) -> str:
        with open(file + ".ass", "w", encoding="utf-8") as f:
            f.write(self.sub.dump())
            PriI('保存于 "{}.ass"', file)
            return file + ".ass"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=_("一个可以把Youtube注释转换成ASS字幕的脚本"))
    parser.add_argument(
        "File", type=str, nargs="+", metavar="File or videoId", help=_("待转换的文件")
    )
    parser.add_argument("-l", "--use-libass", action="store_true", help=_("针对libass修正"))
    parser.add_argument(
        "-x",
        "--reset-resolution-x",
        default=100,
        type=int,
        metavar=100,
        help=_("重设分辨率X"),
    )
    parser.add_argument(
        "-y",
        "--reset-resolution-y",
        default=100,
        type=int,
        metavar=100,
        help=_("重设分辨率Y"),
    )
    parser.add_argument(
        "-f", "--font", default=font, type=str, metavar=font, help=_("指定字体")
    )
    parser.add_argument(
        "-d",
        "--download-for-archive",
        action="store_true",
        help=_("尝试从 Internet Archive 下载注释文件"),
    )
    parser.add_argument(
        "-p", "--preview-video", action="store_true", help=_("预览视频(需要mpv)")
    )
    parser.add_argument(
        "-g", "--generate-video", action="store_true", help=_("生成视频(需要FFmpeg)")
    )
    args = parser.parse_args()
    libass_hack = args.use_libass

    convert_parameter = ConvertParameterStructure()
    convert_parameter.resolution_x = args.reset_resolution_x
    convert_parameter.resolution_y = args.reset_resolution_y
    convert_parameter.font = args.font

    if (args.download_for_archive or args.preview_video or args.generate_video) is True:
        videoIds = []
        for videoId in args.File:
            m = re.match(r"[a-zA-Z0-9_-]{11}", videoId)
            if m != None:
                selected_videoId = m.group()
                PriI("选中{}", selected_videoId)
                videoIds.append(selected_videoId)
            else:
                PriW("无效的videoId: {}", videoId)
        check_network()
        if args.preview_video or args.generate_video is True:
            libass_hack = True
        if len(videoIds) == 0:
            PriW("没有文件要转换")
        for videoId in videoIds:
            File = download_annotations_for_archive(video_id=videoId)
            if File == None:
                PriW("{} 没有注释", videoId)
            convert_parameter.title = File
            convert_parameter.libass_hack = libass_hack
            sub = Annotations2Sub(file=File, convert_parameter=convert_parameter)
            File = sub.Save(file=File)
            del sub
            if args.preview_video is True:
                preview_video(video_id=videoId, file=File)
            if args.generate_video is True:
                generate_video(video_id=videoId, file=File)
    if (
        args.download_for_archive or args.preview_video or args.generate_video
    ) is not True:
        Files = []
        for File in args.File:
            for i in glob.iglob(File):
                if os.path.exists(i):
                    PriI("选中{}", i)
                    Files.append(i)
                else:
                    PriI("文件不存在({})", i)
        if len(Files) == 0:
            PriW("没有文件要转换")
        for File in Files:
            convert_parameter.title = File
            convert_parameter.libass_hack = libass_hack
            sub = Annotations2Sub(file=File, convert_parameter=convert_parameter)
            File = sub.Save(file=File)
            del sub
