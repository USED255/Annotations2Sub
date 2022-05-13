#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
"""

import datetime
from typing import Dict, List

from Annotations2Sub.Color import Alpha, Color, Rgba
from Annotations2Sub.internationalization import _

# 兼容 Python3.6, 3.7
# Python3.6, 3.7 的 typing 没有 Literal
try:
    from typing import Literal  # type: ignore
except:
    pass


class Style:
    """SSA 的样式结构"""

    # ! 带引号的还是从 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 粘过来的 !
    # Name 不在这里面, 因为我想用字典实现
    def __init__(self):
        # "Style 行中的所有设定，除了阴影和边框的类型和深度，都可以被字幕文本中的控制代码所覆写。"

        # "使用的字体名称，区分大小写。"
        self.Fontname: str = "Arial"

        # 一下都用默认值
        self.Fontsize: float = 20
        self.PrimaryColour: Rgba = Rgba(Color(255, 255, 255), Alpha(0))
        self.SecondaryColour: Rgba = Rgba(Color(255, 0, 0), Alpha(0))
        self.OutlineColour: Rgba = Rgba(Color(0, 0, 0), Alpha(0))
        self.BackColour: Rgba = Rgba(Color(0, 0, 0), Alpha(0))
        self.Bold: Literal[-1, 0] = 0
        self.Italic: Literal[-1, 0] = 0
        self.Underline: Literal[-1, 0] = 0
        self.StrikeOut: Literal[-1, 0] = 0
        self.ScaleX: int = 100
        self.ScaleY: int = 100
        self.Spacing: int = 0
        self.Angle: float = 0
        self.BorderStyle: Literal[1, 3] = 1
        self.Outline: Literal[0, 1, 2, 3, 4] = 2
        self.Shadow: Literal[0, 1, 2, 3, 4] = 2
        self.Alignment: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = 2
        self.MarginL: int = 10
        self.MarginR: int = 10
        self.MarginV: int = 10

        # "它定义了字体的字符集或编码方式。"
        # "在多语种的 Windows 安装中它可以获取多种语言中的字符。"
        # "通常 0 为英文，134 为简体中文，136 为繁体中文。"
        # "当文件是 Unicode 编码时，该字段在解析对话时会起作用。"
        # 直接抄 Aegisub 置为 1
        self.Encoding: int = 1


class Event:
    """Sub 的 Event 结构"""

    def __init__(self):
        # 有 Dialogue, Comment, Picture, Sound, Movie, Command 事件
        # 但是我们只用到 Dialogue
        # "这是一个对话事件，即显示一些文本。"
        self.Type: Literal["Dialogue"] = "Dialogue"
        # Aegisub 没有 Marked ,所以我们也没有
        # 剩下的读一下 ./Convert.py 吧
        self.Layer: int = 0
        self.Start: datetime.datetime = datetime.datetime.strptime("0", "%S")
        self.End: datetime.datetime = datetime.datetime.strptime("0", "%S")
        self.Style: str = "Default"
        self.Name: str = ""
        # MarginL, MarginR, MarginV, Effect 在本项目中均没有使用
        self.MarginL: int = 0
        self.MarginR: int = 0
        self.MarginV: int = 0
        self.Effect: str = ""
        self.Text: str = ""


class Sub:
    """ """

    def __init__(self):
        self._info = self.Info()
        self._styles = self.Styles()
        self._events = self.Events()

        self.info = self._info.info
        self.note = self._info.note
        self.styles = self._styles.styles
        self.events = self._events.events

        self.info["Title"] = "Default File"
        self.note.append(_("此脚本使用 Annotations2Sub 生成"))
        self.note.append("https://github.com/USED255/Annotations2Sub")
        self.styles["Default"] = Style()

    class Info:
        """ """

        def __init__(self):
            self.note: List[str] = []
            self.info: Dict[str, str] = {"ScriptType": "v4.00+"}

        def Dump(self) -> str:
            """ """

            s = ""
            s += "[Script Info]" + "\n"
            for i in self.note:
                s += "; " + i + "\n"
            for k, v in self.info.items():
                s += "{}: {}\n".format(k, v)
            s += "\n"
            return s

    class Styles:
        """ """

        def __init__(self):
            self.styles: Dict[str, Style] = {}

        def Dump(self) -> str:
            """ """

            def DumpAABBGGRR(rgba: Rgba) -> str:
                return "&H{:02X}{:02X}{:02X}{:02X}".format(
                    rgba.alpha.alpha, rgba.color.blue, rgba.color.green, rgba.color.red
                )

            s = ""
            s += "[V4+ Styles]" + "\n"
            s += (
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"
                + "\n"
            )
            for name, each in self.styles.items():
                s += "Style: "
                s += name + ","
                s += each.Fontname + ","
                s += str(each.Fontsize) + ","
                s += DumpAABBGGRR(each.PrimaryColour) + ","
                s += DumpAABBGGRR(each.SecondaryColour) + ","
                s += DumpAABBGGRR(each.OutlineColour) + ","
                s += DumpAABBGGRR(each.BackColour) + ","
                s += str(each.Bold) + ","
                s += str(each.Italic) + ","
                s += str(each.Underline) + ","
                s += str(each.StrikeOut) + ","
                s += str(each.ScaleX) + ","
                s += str(each.ScaleY) + ","
                s += str(each.Spacing) + ","
                s += str(each.Angle) + ","
                s += str(each.BorderStyle) + ","
                s += str(each.Outline) + ","
                s += str(each.Shadow) + ","
                s += str(each.Alignment) + ","
                s += str(each.MarginL) + ","
                s += str(each.MarginR) + ","
                s += str(each.MarginV) + ","
                s += str(each.Encoding) + "\n"
            s += "\n"
            return s

    class Events:
        """ """

        def __init__(self):
            self.events: List[Event] = []

        def Dump(self) -> str:
            """ """

            def DumpTime(t: datetime.datetime) -> str:
                return t.strftime("%H:%M:%S.%f")[:-4]

            s = ""
            s += "[Events]" + "\n"
            s += (
                "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
                + "\n"
            )
            for each in self.events:
                s += "Dialogue: "
                s += str(each.Layer) + ","
                s += DumpTime(each.Start) + ","
                s += DumpTime(each.End) + ","
                s += each.Style + ","
                s += each.Name + ","
                s += str(each.MarginL) + ","
                s += str(each.MarginR) + ","
                s += str(each.MarginV) + ","
                s += each.Effect + ","
                s += each.Text + "\n"
            s += "\n"
            return s

    def Dump(self) -> str:
        """ """

        s = ""
        s += self._info.Dump()
        s += self._styles.Dump()
        s += self._events.Dump()
        return s


class DrawCommand:
    """ """

    def __init__(self, x=0, y=0, command="m"):
        self.x: int = x
        self.y: int = y
        # 这里仅列出需要的命令
        self.command: Literal["m", "l"] = command


class Draw:
    """ """

    def __init__(self):
        self.draw: List[DrawCommand] = []

    def Add(self, command: DrawCommand):
        """ """

        if isinstance(command, DrawCommand) is False:
            raise TypeError("command must be DrawCommand")
        self.draw.append(command)

    def Dump(self) -> str:
        """ """

        s = ""
        for i in self.draw:
            s = s + "{} {} {} ".format(i.command, i.x, i.y)
        return s
