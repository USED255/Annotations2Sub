#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""SSA 相关"""

import datetime
from typing import Dict, List

from Annotations2Sub.Color import Alpha, Color, Rgba
from Annotations2Sub.internationalization import _

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
    """单个 SSA 样式(Style) 结构"""

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
    """单个 SSA 事件(Event) 结构"""

    def __init__(self):
        # 有 Dialogue, Comment, Picture, Sound, Movie, Command 事件
        # 但是我们只用到了 Dialogue
        # "这是一个对话事件，即显示一些文本。"
        self.Type: Literal["Dialogue"] = "Dialogue"
        # Aegisub 没有 Marked, 所以我们也没有
        # 剩下的就读一下 ./Convert.py 吧
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
        self._info = self.Info()
        self._styles = self.Styles()
        self._events = self.Events()

        # 我想让他们直接操作列表或字典
        self.info = self._info.info
        self.note = self._info.note
        self.styles = self._styles.styles
        self.events = self._events.events

        # "标题，对脚本的描述。如果未指定，自动设置为 <untitled>。"
        self.info["Title"] = "Default File"
        # Aegisub 开头也有着这一段
        # 我也学学
        self.note.append(_("此脚本使用 Annotations2Sub 生成"))
        self.note.append("https://github.com/USED255/Annotations2Sub")
        # 定义默认样式
        self.styles["Default"] = Style()

    class Info:
        """SSA 的信息(Info) 结构"""

        def __init__(self):
            # 好像流行开头来一段注释的样子
            self.note: List[str] = []
            # 不言而喻
            # 详细的读 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
            self.info: Dict[str, str] = {"ScriptType": "v4.00+"}

        def Dump(self) -> str:
            """将 Info 结构转换为字符串"""

            # 只是暴力拼接字符串而已
            s = ""
            s += "[Script Info]" + "\n"
            for i in self.note:
                s += "; " + i + "\n"
            for k, v in self.info.items():
                s += "{}: {}\n".format(k, v)
            s += "\n"
            return s

    # 这次和之前相比把一个类拆成了单个结构和一个有 Dump 方法的类
    class Styles:
        def __init__(self):
            self.styles: Dict[str, Style] = {}

        def Dump(self) -> str:
            def DumpAABBGGRR(rgba: Rgba) -> str:
                """转换为 SSA 颜色字符串"""

                # "长整型 BGR（蓝绿红）值，还包含了 alpha 通道信息。"
                # "该值的十六进制字节顺序为 AABBGGRR。例如，&H00FFFFFF。"
                return "&H{:02X}{:02X}{:02X}{:02X}".format(
                    rgba.alpha.alpha, rgba.color.blue, rgba.color.green, rgba.color.red
                )

            # 还是暴力拼接字符串而已
            # 建议阅读: https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
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
        def __init__(self):
            self.events: List[Event] = []

        def Dump(self) -> str:
            def DumpTime(t: datetime.datetime) -> str:
                """转换为 SSA 时间字符串"""

                # "格式为 0:00:00:00（小时:分:秒:毫秒）"
                return t.strftime("%H:%M:%S.%f")[:-4]

            # 建议找个字幕文件看一看
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
        """转储为 SSA"""
        s = ""
        s += self._info.Dump()
        s += self._styles.Dump()
        s += self._events.Dump()
        return s


class DrawCommand:
    """单个绘图指令"""

    def __init__(self, x: float = 0, y: float = 0, command: Literal["m", "l"] = "m"):
        self.x: float = x
        self.y: float = y
        # 这里仅列出需要的命令
        # m, n, l, b, s, p, c
        self.command: Literal["m", "l"] = command


class Draw:
    """绘图类"""

    def __init__(self):
        self.draw: List[DrawCommand] = []

    def Add(self, command: DrawCommand):
        """添加一个绘图指令"""
        if isinstance(command, DrawCommand) is False:
            raise TypeError("command must be DrawCommand")
        self.draw.append(command)

    def Dump(self) -> str:
        """转储为绘图命令"""

        # 建议下一个 Aegisub 然后打开 ASSDraw3 画画玩玩
        s = ""
        for i in self.draw:
            s = s + "{} {} {} ".format(i.command, i.x, i.y)
        return s
