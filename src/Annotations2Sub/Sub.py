#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""SSA 相关"""

import datetime
from typing import Dict, List

from Annotations2Sub.Color import Alpha, Color, Rgba


def Dummy(*args, **kwargs):
    """用于 MonkeyPatch"""


# 兼容 Python3.6, 3.7
# Python3.6, 3.7 的 typing 没有 Literal
try:
    from typing import Literal  # type: ignore
except ImportError:

    class a:
        def __getitem__(self, b):
            return b

    exec("Literal = a()")


class Style:
    """SSA 样式(Style) 结构"""

    def __init__(self):
        # 带引号的是从 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 粘过来的
        # Name 不在这里, 它会这样出现 Dict[Name:str, Style:Style]

        # "Style 行中的所有设定，除了阴影和边框的类型和深度，都可以被字幕文本中的控制代码所覆写。"
        # "使用的字体名称，区分大小写。"
        self.Fontname: str = "Arial"

        # 本项目的样式都用样式复写标签实现, 这些字段不会用到
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
    """SSA 事件(Event) 结构"""

    def __init__(self):
        # 有 Dialogue, Comment, Picture, Sound, Movie, Command 事件
        # 只用到了 Dialogue
        # "这是一个对话事件，即显示一些文本。"
        self.Type: Literal["Dialogue"] = "Dialogue"
        # Aegisub 没有 Marked, 所以我们也没有
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
    """SSA 类"""

    def __init__(self):
        self._info = self._Info()
        self._styles = self._Styles()
        self._events = self._Events()

        # 我想让他们直接操作列表或字典
        self.info = self._info.infos
        self.comment = ""
        self.styles = self._styles.styles
        self.events = self._events.events

        # "标题，对脚本的描述。如果未指定，自动设置为 <untitled>。"
        self.info["Title"] = "Default File"
        # 定义默认样式
        self.styles["Default"] = Style()

    def __str__(self) -> str:
        return self.Dump()

    def Dump(self) -> str:
        """转储为 SSA"""
        self._info.comment = self.comment

        string = ""
        string += self._info.Dump()
        string += self._styles.Dump()
        string += self._events.Dump()
        return string

    class _Info:
        """SSA 的信息(Info) 结构"""

        def __init__(self):
            # 好像流行开头来一段注释的样子
            self.comment: str = ""
            # 必要的字段
            self.infos: Dict[str, str] = {"ScriptType": "v4.00+"}

        def __str__(self) -> str:
            return self.Dump()

        def Dump(self) -> str:
            """将 Info 结构转换为字符串"""

            # 只是暴力拼接字符串而已
            string = ""
            string += "[Script Info]\n"
            if self.comment != "":
                for line in self.comment.split("\n"):
                    string += f"; {line}\n"
            for k, v in self.infos.items():
                string += f"{k}: {v}\n"
            string += "\n"
            return string

    # 这次和之前相比把一个类拆成了结构和一个 Dump 方法
    class _Styles:
        def __init__(self):
            self.styles: Dict[str, Style] = {}

        def __str__(self) -> str:
            return self.Dump()

        def Dump(self) -> str:
            def DumpAABBGGRR(rgba: Rgba) -> str:
                """转换为 SSA 颜色字符串"""

                # "长整型 BGR（蓝绿红）值，还包含了 alpha 通道信息。"
                # "该值的十六进制字节顺序为 AABBGGRR。例如，&H00FFFFFF。"
                return "&H{:02X}{:02X}{:02X}{:02X}".format(
                    rgba.alpha, rgba.blue, rgba.green, rgba.red
                )

            string = ""
            string += "[V4+ Styles]\n"
            string += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"

            for Name, Styles in self.styles.items():
                string += f"Style: {Name},{Styles.Fontname},{Styles.Fontsize},{DumpAABBGGRR(Styles.PrimaryColour)},{DumpAABBGGRR(Styles.SecondaryColour)},{DumpAABBGGRR(Styles.OutlineColour)},{DumpAABBGGRR(Styles.BackColour)},{Styles.Bold},{Styles.Italic},{Styles.Underline},{Styles.StrikeOut},{Styles.ScaleX},{Styles.ScaleY},{Styles.Spacing},{Styles.Angle},{Styles.BorderStyle},{Styles.Outline},{Styles.Shadow},{Styles.Alignment},{Styles.MarginL},{Styles.MarginR},{Styles.MarginV},{Styles.Encoding}\n"
            string += "\n"
            return string

    class _Events:
        def __init__(self):
            self.events: List[Event] = []

        def __str__(self) -> str:
            return self.Dump()

        def Dump(self) -> str:
            def DumpTime(t: datetime.datetime) -> str:
                """转换为 SSA 时间字符串"""

                # "格式为 0:00:00:00（小时:分:秒:毫秒）"
                return t.strftime("%H:%M:%S.%f")[:-4]

            string = ""
            string += "[Events]\n"
            string += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

            for Event in self.events:
                string += f"Dialogue: {Event.Layer},{DumpTime(Event.Start)},{DumpTime(Event.End)},{Event.Style},{Event.Name},{Event.MarginL},{Event.MarginR},{Event.MarginV},{Event.Effect},{Event.Text}\n"
            string += "\n"
            return string


class DrawCommand:
    """绘图指令结构"""

    def __init__(self, x: float = 0, y: float = 0, command: Literal["m", "l"] = "m"):
        self.x: float = x
        self.y: float = y
        # 命令有 m, n, l, b, s, p, c
        # 这里仅列出需要的命令
        self.command: Literal["m", "l"] = command


class Draw:
    """绘图类"""

    def __init__(self):
        self.draws: List[DrawCommand] = []

    def __str__(self) -> str:
        return self.Dump()

    def Add(self, command: DrawCommand):
        """添加一个绘图指令"""
        if isinstance(command, DrawCommand) is False:
            raise TypeError("command must be DrawCommand")
        self.draws.append(command)

    def Dump(self) -> str:
        """转储为绘图命令"""

        # "所有绘图都应由 m <x> <y> 命令开头"
        # "所有没闭合的图形会被自动地在起点和终点之间添加直线来闭合。"
        # "如果一个对话行中的多个图形有重叠，重叠部分会进行异或运算。"
        string = ""
        for draw in self.draws:
            string = string + f"{draw.command} {draw.x} {draw.y} "
        return string
