#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from typing import Literal, List, Optional
from xml.etree.ElementTree import Element

from Annotations2Sub.Color import Alpha, Color
from Annotations2Sub.locale import _


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


def Parse(tree: Element) -> List[Annotation]:
    """XML 树转换为 Annotation 结构列表"""

    def ParseAnnotationAlpha(annotation_alpha_str: str) -> Alpha:
        """
        解析 Annotation 的透明度
        bgAlpha="0.600000023842" -> Alpha(alpha=102)
        """
        s0 = annotation_alpha_str
        if s0 == None:
            raise Exception("alpha is None")
        s1 = float(s0)
        s2 = 1 - s1
        s3 = s2 * 255
        s4 = int(s3)
        s5 = Alpha(alpha=s4)
        return s5

    def ParseAnnotationColor(annotation_color_str: str) -> Color:
        """
        bgColor="4210330" -> Color(red=154, green=62, blue=64)
        """
        s0 = annotation_color_str
        if s0 == None:
            raise Exception("color is None")
        s1 = int(s0)
        r = s1 & 255
        g = (s1 >> 8) & 255
        b = s1 >> 16
        s2 = Color(red=r, green=g, blue=b)
        return s2

    def MakeSureStr(s: Optional[str]) -> str:
        if isinstance(s, str):
            return str(s)
        raise TypeError

    def ParseAnnotation(each: Element) -> Optional[Annotation]:
        # 致谢: https://github.com/nirbheek/youtube-ass
        # 致谢: https://github.com/isaackd/annotationlib
        annotation = Annotation()

        annotation.id = MakeSureStr(each.get("id"))

        type = each.get("type")
        if type not in ("text", "highlight", "branding"):
            print(_("不支持{}类型. ()").format(type, annotation.id))
            return None
        annotation.type = MakeSureStr(type)  # type: ignore

        annotation.style = each.get("style")  # type: ignore

        text = each.find("TEXT")
        if text is None:
            annotation.text = ""
        else:
            annotation.text = MakeSureStr(text.text)

        if len(each.find("segment").find("movingRegion")) == 0:  # type: ignore
            # 跳过没有内容的 Annotation
            return None

        Segment = each.find("segment").find("movingRegion").findall("rectRegion")  # type: ignore
        if len(Segment) == 0:
            Segment = (
                each.find("segment").find("movingRegion").findall("anchoredRegion")  # type: ignore
            )

        if len(Segment) == 0:
            if annotation.style != "highlightText":
                # 抄自 https://github.com/isaackd/annotationlib/blob/master/src/parser/index.js 第121行
                # "highlightText" 是一直显示在屏幕上的, 不应没有时间
                return None

        if len(Segment) != 0:
            t1 = MakeSureStr(Segment[0].get("t"))
            t2 = MakeSureStr(Segment[1].get("t"))
            Start = min(t1, t2)
            End = max(t1, t2)

        if "never" in (Start, End):
            # 跳过不显示的 Annotation
            return None

        try:
            annotation.timeStart = datetime.datetime.strptime(Start, "%H:%M:%S.%f")
            annotation.timeEnd = datetime.datetime.strptime(End, "%H:%M:%S.%f")
        except:
            annotation.timeStart = datetime.datetime.strptime(Start, "%M:%S.%f")
            annotation.timeEnd = datetime.datetime.strptime(End, "%M:%S.%f")

        annotation.x = float(MakeSureStr(Segment[0].get("x")))
        annotation.y = float(MakeSureStr(Segment[0].get("y")))

        w = Segment[0].get("w")
        h = Segment[0].get("h")
        sx = Segment[0].get("sx")
        sy = Segment[0].get("sy")

        if w is not None:
            annotation.width = float(MakeSureStr(w))
        if h is not None:
            annotation.height = float(MakeSureStr(h))
        if sx is not None:
            annotation.sx = float(MakeSureStr(sx))
        if sy is not None:
            annotation.sy = float(MakeSureStr(sy))

        Appearance = each.find("appearance")

        if Appearance != None:
            bgAlpha = Appearance.get("bgAlpha")  # type: ignore
            bgColor = Appearance.get("bgColor")  # type: ignore
            fgColor = Appearance.get("fgColor")  # type: ignore
            textSize = Appearance.get("textSize")  # type: ignore

        if bgAlpha != None:
            annotation.bgOpacity = ParseAnnotationAlpha(MakeSureStr(bgAlpha))
        if bgColor != None:
            annotation.bgColor = ParseAnnotationColor(MakeSureStr(bgColor))
        if fgColor != None:
            annotation.fgColor = ParseAnnotationColor(MakeSureStr(fgColor))
        if textSize != None:
            annotation.textSize = float(MakeSureStr(textSize))

        return annotation

    annotations: List[Annotation] = []
    for each in tree.find("annotations").findall("annotation"):  # type: ignore
        annotation = ParseAnnotation(each)
        if annotation != None:
            annotations.append(annotation)  # type: ignore

    return annotations
