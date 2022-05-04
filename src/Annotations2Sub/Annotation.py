#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from typing import Literal

from Annotations2Sub.Color import Alpha, Color


class Annotation(object):
    # 致谢 https://github.com/isaackd/annotationlib
    """Annotation 结构"""

    def __init__(self):
        # 仅列出了需要的结构
        self.id: str = ""
        # 这里仅列出需要的的 type 和 style
        self.type: Literal["text", "highlight", "branding"] = ""
        self.style: Literal[
            "popup",
            "title",
            "speech",
            "highlightText",
        ] = ""
        self.text: str = ""
        self.timeStart: datetime.datetime = datetime.datetime.strptime("0", "%S")
        self.timeEnd: datetime.datetime = datetime.datetime.strptime("0", "%S")
        self.x: float = 0.0
        self.y: float = 0.0
        self.width: float = 0.0
        self.height: float = 0.0
        # sx, sy 是气泡锚点
        self.sx: float = 0.0
        self.sy: float = 0.0
        self.bgOpacity: Alpha = Alpha(alpha=204)
        self.bgColor: Color = Color(red=255, green=255, blue=255)
        self.fgColor: Color = Color(red=0, green=0, blue=0)
        self.textSize: float = 3.15
