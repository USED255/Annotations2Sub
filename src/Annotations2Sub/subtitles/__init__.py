# -*- coding: utf-8 -*-

from Annotations2Sub.subtitles import tag
from Annotations2Sub.subtitles.draw import Draw, DrawCommand
from Annotations2Sub.subtitles.event import Event
from Annotations2Sub.subtitles.style import Style
from Annotations2Sub.subtitles.subtitles import Subtitles

__all__ = [
    "Subtitles",
    "Style",
    "Event",
    "Draw",
    "DrawCommand",
    "tag",
]

# ASS 字幕是一种常见的外挂字幕格式, 全称 Advanced SubStation Alpha.
# 与其他字幕格式相比, 他能够设置字体、颜色、位置, 甚至添加图像和特效, 增强您的观看体验.

# 这个包里的文件中带引号的注释是从
# https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
# 粘过来的, 例如:
# "Sub Station Alpha 本身是一个 Windows 平台下制作 SSA 格式字幕的软件，该软件已经不再开发了，而它所创造的 SSA 格式却流行开来，并演化出了更先进的 ASS 格式。"
# "目前 ASS 字幕制作人员所看到的效果绝大多数都是由 xy-VSFilter 和 libass 渲染的，于是这两个渲染器就成了事实上的标准。"
# 我在写代码时大量参考了这个文档, 对我帮助很大, 非常感谢 Zhenye Wei 的工作.
