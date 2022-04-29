#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Color(object):
    """以 0-255 的整数表示颜色值, 不提供序列化方法"""

    def __init__(
        self,
        red: int = 0,
        green: int = 0,
        blue: int = 0,
    ):
        self.red = red
        self.green = green
        self.blue = blue


class Alpha(object):
    """以 0-255 的整数表示透明度, 不提供序列化方法"""

    def __init__(
        self,
        alpha: int = 0,
    ):
        self.alpha = alpha
