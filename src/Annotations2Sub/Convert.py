#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from typing import List, Optional
from  xml.etree.ElementTree import Element
from . import *


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

    def White() -> Color:
        return Color(red=255, green=255, blue=255)

    def Black() -> Color:
        return Color(red=0, green=0, blue=0)

    def DefaultTransparency() -> Alpha:
        return Alpha(alpha=204)

    def ParseAnnotation(each: Element) -> Optional[Annotation]:
        # 致谢 https://github.com/nirbheek/youtube-ass
        # 致谢 https://github.com/isaackd/annotationlib
        annotation = Annotation()

        annotation.id = each.get("id")

        type = each.get("type")

        if type is None or type == "pause":
            # Sub 无法实现 "pause", 跳过
            return None

        annotation.type = type

        annotation.style = each.get("style")

        annotation.text = each.find("TEXT")

        if len(each.find("segment").find("movingRegion")) == 0:
            # 跳过没有内容的 Annotation
            return None

        Segment = each.find("segment").find("movingRegion").findall("rectRegion")
        if len(Segment) == 0:
            Segment = (
                each.find("segment").find("movingRegion").findall("anchoredRegion")
            )

        if len(Segment) == 0:
            if annotation.style != "highlightText":
                # 抄自 https://github.com/isaackd/annotationlib/blob/master/src/parser/index.js 第121行
                # "highlightText" 是一直显示在屏幕上的, 不应没有时间
                return None

        if len(Segment) != 0:
            Start = min(Segment[0].get("t"), Segment[1].get("t"))
            End = max(Segment[0].get("t"), Segment[1].get("t"))

        if "never" in (Start, End):
            # 跳过不显示的 Annotation
            return None

        try:
            annotation.timeStart = datetime.strptime(Start, "%H:%M:%S.%f")
            annotation.timeEnd = datetime.strptime(End, "%H:%M:%S.%f")
        except:
            annotation.timeStart = datetime.strptime(Start, "%M:%S.%f")
            annotation.timeEnd = datetime.strptime(End, "%M:%S.%f")

        annotation.x = float(Segment[0].get("x"))
        annotation.y = float(Segment[0].get("y"))
        annotation.width = float(Segment[0].get("w"))
        annotation.height = float(Segment[0].get("h"))
        annotation.sx = float(Segment[0].get("sx"))
        annotation.sy = float(Segment[0].get("sy"))

        Appearance = each.find("appearance")

        if Appearance != None:
            bgAlpha = Appearance.get("bgAlpha")
            bgColor = Appearance.get("bgColor")
            fgColor = Appearance.get("fgColor")
            textSize = Appearance.get("textSize")

        if bgAlpha != None:
            annotation.bgOpacity = ParseAnnotationAlpha(bgAlpha)
        else:
            annotation.bgOpacity = DefaultTransparency()

        if bgColor != None:
            annotation.bgColor = ParseAnnotationColor(bgColor)
        else:
            annotation.bgColor = White()

        if fgColor != None:
            annotation.fgColor = ParseAnnotationColor(fgColor)
        else:
            annotation.fgColor = Black()

        if textSize != None:
            annotation.textSize = float(textSize)
        else:
            annotation.textSize = 3.15

        return annotation

    annotations: List[Annotation] = []
    for each in tree.find("annotations").findall("annotation"):
        annotation = ParseAnnotation(each)
        if annotation != None:
            annotations.append(annotation)

    return annotations
