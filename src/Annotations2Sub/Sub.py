#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
"""

import datetime
from typing import List, Literal


class Event:
    """Sub 的 Event 结构"""

    def __init__(self):

        # 仅列出了需要的 Format
        self.Format: Literal["Dialogue"] = ("Dialogue",)
        # Aegisub 没有 Marked ,所以我们也没有
        self.Layer: int = (0,)
        self.Start: datetime.datetime = datetime.datetime()
        self.End: datetime.datetime = datetime.datetime()
        self.Style: str = ("Default",)
        self.Name: str = ("",)
        # MarginL, MarginR, MarginV, Effect 在本项目中均没有使用
        self.MarginL: int = (0,)
        self.MarginR: int = (0,)
        self.MarginV: int = (0,)
        self.Effect: str = ("",)
        self.Text: str = ("",)


class Point:
    """绘图命令"""

    def __init__(self, x=0, y=0, command="m"):
        self.x: int = x
        self.y: int = y
        # 仅列出需要的命令
        self.command: Literal["m", "l"] = command


class Draw:
    def __init__(self):
        self.draw: List[Point] = []

    def Add(self, point: Point):
        self.draw.append(point)

    def Dump(self) -> str:
        s = ""
        for i in self.draw:
            s = s + "{} {} {} ".format(i.command, i.x, i.y)
        return s
