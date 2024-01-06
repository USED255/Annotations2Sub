#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""样式复写代码, 样式复写标签, ASS 标签, 特效标签, Aegisub 特效标签, 标签"""

from Annotations2Sub.Color import Alpha, Color

# 带引号的是从 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 粘过来的


def DumpColor(color: Color) -> str:
    """将 Color 转换为 SSA 的颜色表示"""
    return "&H{:02X}{:02X}{:02X}&".format(color.red, color.green, color.blue)


def DumpAlpha(alpha: Alpha) -> str:
    """将 Alpha 转换为 SSA 的 Alpha 表示"""

    # 据 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 所说
    # SSA 的 Alpha 是透明度, 00 为不透明，FF 为全透明
    return "&H{:02X}&".format(255 - alpha.alpha)


class Tag(list):
    def __str__(self) -> str:
        tag_string = ""
        for tag in self:
            tag_string += str(tag)
        tag_string = r"{" + tag_string + r"}"
        return tag_string

    class Pos:
        r"""\an<位置>"""

        # "<位置> 是一个数字，决定了字幕显示在屏幕上哪个位置。"
        # 默认 SSA 定位会定在文本中间
        # 用 \an7 指定在左上角.
        # "\pos(<x>,<y>)"
        # "将字幕定位在坐标点 <x>,<y>。"
        # SSA 和 Annotations 坐标系一致, y 向下(左手取向).
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

        def __str__(self) -> str:
            return rf"\an7\pos({self.x},{self.y})"

    class Fontsize:
        r"""\fs<字体尺寸>"""

        # "<字体尺寸> 是一个数字，指定了字体的点的尺寸。"
        # "注意，这里的字体尺寸并不是字号的大小，\fs20 并不是字体大小（font-size）为 20px，"
        # "而是指其行高（line-height）为 20px，主要归咎于 VSFilter 使用的 Windows GDI 的字体接口。"
        # 不明白字体大小和行高有什么区别
        def __init__(self, size: float):
            self.size = size

        def __str__(self) -> str:
            return r"\fs" + str(self.size)

    class PrimaryColour:
        r"""\<颜色序号>c[&][H]<BBGGRR>[&]"""

        # "<BBGGRR> 是一个十六进制的 RGB 值，但颜色顺序相反，前导的 0 可以省略。"
        # "<颜色序号> 可选值为 1、2、3 和 4，分别对应单独设置 PrimaryColour、SecondaryColour、OutlineColor 和 BackColour"
        # "其中的 & 和 H 按规范应该是要有的，但是如果没有也能正常解析。"
        # PrimaryColour 填充颜色, SecondaryColour 卡拉OK变色, OutlineColor 边框颜色, BackColour 阴影颜色
        def __init__(self, colour: Color):
            self.colour = colour

        def __str__(self) -> str:
            return r"\c" + DumpColor(self.colour)

    class PrimaryAlpha:
        r"""\<颜色序号>a[&][H]<AA>[&]"""

        # "<AA> 是一个十六进制的透明度数值，00 为全见，FF 为全透明。"
        # "<颜色序号> 含义同上，但这里不能省略。写法举例：\1a&H80&、\2a&H80、\3a80、\4a&H80&。"
        # "其中的 & 和 H 按规范应该是要有的，但是如果没有也能正常解析。"
        # Annotations 文本好像没有透明度, 这个很符合直觉
        def __init__(self, alpha: Alpha):
            self.alpha = alpha

        def __str__(self) -> str:
            return r"\1a" + DumpAlpha(self.alpha)

    class Bold:
        def __init__(self, bold: float):
            self.bold = bold

        def __str__(self) -> str:
            return r"\b" + str(self.bold)

    class Bord:
        def __init__(self, bord: float):
            self.bord = bord

        def __str__(self) -> str:
            return r"\bord" + str(self.bord)

    class Shadow:
        def __init__(self, shadow: float):
            self.shadow = shadow

        def __str__(self) -> str:
            return r"\shad" + str(self.shadow)
