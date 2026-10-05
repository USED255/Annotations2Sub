# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Color:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class Alpha:
    alpha: int = 0


@dataclass
class Rgba:
    def __init__(self, color: Color = Color(), alpha: Alpha = Alpha()):
        self.red = color.red
        self.green = color.green
        self.blue = color.blue
        self.alpha = alpha.alpha
