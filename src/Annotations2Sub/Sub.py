#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
"""

import datetime
from typing import List, Literal
from . import *


class Event:
    def __init__(self):

        # 仅列出了需要的 Format
        self.Format: Literal["Dialogue"] = ("Dialogue",)
        # Aegisub 没有 Marked ,所以我们也没有
        self.Layer: int = (0,)
        self.Start: datetime.datetime = datetime.datetime()
        self.End: datetime.datetime = datetime.datetime()
        self.Style: str = ("Default",)
        self.Name: str = ("",)
        # MarginL, MarginR, MarginV, Effect 均没有使用
        self.MarginL: int = (0,)
        self.MarginR: int = (0,)
        self.MarginV: int = (0,)
        self.Effect: str = ("",)
        self.Text: str = ("",)


class Point:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        # 进列出需要的命令
        self.command: Literal["m", "l"] = "m"


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
