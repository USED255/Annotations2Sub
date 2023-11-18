#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""颜色数据类"""


class Color:
    def __init__(
        self,
        red: int = 0,
        green: int = 0,
        blue: int = 0,
    ):
        if red > 255:
            raise ValueError("red must be 0-255")
        if green > 255:
            raise ValueError("green must be 0-255")
        if blue > 255:
            raise ValueError("blue must be 0-255")
        self.red = red
        self.green = green
        self.blue = blue


class Alpha:
    def __init__(
        self,
        alpha: int = 0,
    ):
        if alpha > 255:
            raise ValueError("alpha must be 0-255")
        self.alpha = alpha


class Rgba:
    def __init__(self, color: Color = Color(), alpha: Alpha = Alpha()):
        self.color = color
        self.alpha = alpha
