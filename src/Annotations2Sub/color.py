# -*- coding: utf-8 -*-

from Annotations2Sub.i18n import _


class Color:
    def __init__(
        self,
        red: int = 0,
        green: int = 0,
        blue: int = 0,
    ):
        if red > 255:
            raise ValueError(_('"red" 必须在 0-255 之间'))
        if green > 255:
            raise ValueError(_('"green" 必须在 0-255 之间'))
        if blue > 255:
            raise ValueError(_('"blue" 必须在 0-255 之间'))
        self.red = red
        self.green = green
        self.blue = blue


class Alpha:
    def __init__(self, alpha: int = 0):
        if alpha > 255:
            raise ValueError(_('"alpha" 必须在 0-255 之间'))
        self.alpha = alpha


class Rgba:
    def __init__(self, color: Color = Color(), alpha: Alpha = Alpha()):
        self.red = color.red
        self.green = color.green
        self.blue = color.blue
        self.alpha = alpha.alpha
