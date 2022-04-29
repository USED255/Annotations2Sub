#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from typing import Literal, Optional
from . import *


class Annotation(object):
    # 致谢 https://github.com/isaackd/annotationlib
    """Annotation 结构"""

    def __init__(self):
        self.id: str = ""
        # 这里仅列出需要的的 type 和 style
        self.type: Literal["text", "highlight", "branding"] = ""
        self.style: Literal[
            "popup",
            "title",
            "speech",
            "highlightText",
        ] = ""
        self.text: Optional[str] = ""
        self.timeStart: datetime.datetime = datetime.datetime()
        self.timeEnd: datetime.datetime = datetime.datetime()
        self.x: Optional[float] = 0.0
        self.y: Optional[float] = 0.0
        self.width: Optional[float] = 0.0
        self.height: Optional[float] = 0.0
        # sx, sy 是气泡锚点
        self.sx: Optional[float] = 0.0
        self.sy: Optional[float] = 0.0
        self.bgOpacity: Optional[Alpha] = Alpha()
        self.bgColor: Optional[Color] = Color()
        self.fgColor: Optional[Color] = Color()
        self.textSize: Optional[float] = 0.0
        # Sub 无法实现 action
        # self.actionType: Optional[str] = ''
        # self.actionUrl: Optional[str] = ''
        # self.actionUrlTarget: Optional[str] = ''
        # self.actionSeconds: Optional[float] = 0.0
        # self.highlightId: Optional[str] = ''


