#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Annotations2Sub.Color import Alpha, Color


def DumpColor(color: Color) -> str:
    """将 Color 转换为 SSA 的颜色表示"""
    return "&H{:02X}{:02X}{:02X}&".format(color.red, color.green, color.blue)


def DumpAlpha(alpha: Alpha) -> str:
    """将 Alpha 转换为 SSA 的 Alpha 表示"""

    # 据 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 所说
    # SSA 的 Alpha 是透明度, 00 为不透明，FF 为全透明
    return "&H{:02X}&".format(255 - alpha.alpha)


class Tag:
    class Pos:
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

        def __str__(self) -> str:
            return rf"\an7\pos({self.x},{self.y})"

    class PrimaryColour:
        def __init__(self, colour: Color):
            self.colour = colour

        def __str__(self) -> str:
            return r"\c" + DumpColor(self.colour)

    class Fontsize:
        def __init__(self, size: float):
            self.size = size

        def __str__(self) -> str:
            return r"\fs" + str(self.size)

    class PrimaryAlpha:
        def __init__(self, alpha: Alpha):
            self.alpha = alpha

        def __str__(self) -> str:
            return r"\1a" + DumpAlpha(self.alpha)

    class SecondaryAlpha:
        def __init__(self, alpha: Alpha):
            self.alpha = alpha

        def __str__(self) -> str:
            return r"\2a" + DumpAlpha(self.alpha)

    class BorderAlpha:
        def __init__(self, alpha: Alpha):
            self.alpha = alpha

        def __str__(self) -> str:
            return r"\3a" + DumpAlpha(self.alpha)

    class ShadowAlpha:
        def __init__(self, alpha: Alpha):
            self.alpha = alpha

        def __str__(self) -> str:
            return r"\4a" + DumpAlpha(self.alpha)

    class Builder:
        def __init__(self, text: str):
            self.text = text
            self.tags: list = []

        def __str__(self) -> str:
            tag = ""
            for i in self.tags:
                tag += str(i)
            tag = r"{" + tag + r"}"
            return tag + self.text
