#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from typing import List, Literal, Optional
import defusedxml.ElementTree as ET


class Color(object):
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
    def __init__(
        self,
        alpha: int = 0,
    ):
        self.alpha = alpha


class Annotation(object):
    def __init__(self):
        self.id: str = ""
        self.type: Literal["text", "highlight", "pause", "branding"] = ""
        self.style: Literal["popup", "title", "speech"] = ""
        self.text: Optional[str] = ""
        self.timeStart: datetime.datetime = datetime.datetime()
        self.timeEnd: datetime.datetime = datetime.datetime()
        self.x: Optional[float] = 0.0
        self.y: Optional[float] = 0.0
        self.width: Optional[float] = 0.0
        self.height: Optional[float] = 0.0
        self.sx: Optional[float] = 0.0
        self.sy: Optional[float] = 0.0
        self.bgOpacity: Optional[Alpha] = Alpha()
        self.bgColor: Optional[Color] = Color()
        self.fgColor: Optional[Color] = Color()
        self.textSize: Optional[float] = 0.0
        # self.actionType: Optional[str] = ''
        # self.actionUrl: Optional[str] = ''
        # self.actionUrlTarget: Optional[str] = ''
        # self.actionSeconds: Optional[float] = 0.0


def XmlTreeToAnnotationStructureList(xml_tree: ET) -> List[Annotation]:
    def ConvertAlpha(annotation_alpha_str: str) -> Alpha:
        s0 = annotation_alpha_str
        if s0 == None:
            raise Exception("alpha is None")
        s1 = float(s0)
        s2 = 1 - s1
        s3 = s2 * 255
        s4 = int(s3)
        s5 = Alpha(alpha=s4)
        return s5

    def ConvertColor(annotation_color_str: str) -> Color:
        s0 = annotation_color_str
        if s0 == None:
            raise Exception("color is None")
        s1 = int(s0)
        r = s1 >> 16
        g = (s1 >> 8) & 0xFF
        b = s1 & 0xFF
        s2 = Color(red=r, green=g, blue=b)
        return s2

    def White() -> Color:
        return Color(red=255, green=255, blue=255)

    def Black() -> Color:
        return Color(red=0, green=0, blue=0)

    def DefaultTransparency() -> Alpha:
        return Alpha(alpha=204)

    annotations: List[Annotation] = []
    for each in xml_tree:
        annotation = Annotation()
        annotation.id = each.get("id")
        annotation.type = each.get("type")
        annotation.style = each.get("style")
        annotation.text = each.find("TEXT")
        _Segment = each.find("segment").find("movingRegion").findall("rectRegion")
        if len(_Segment) == 0:
            _Segment = (
                each.find("segment").find("movingRegion").findall("anchoredRegion")
            )
        if len(_Segment) == 0:
            pass
        if len(_Segment) != 0:
            Start = min(_Segment[0].get("t"), _Segment[1].get("t"))
            End = max(_Segment[0].get("t"), _Segment[1].get("t"))
        if "never" in (Start, End):
            annotation.timeEnd = datetime.strptime("999", "%H")
        if not "never" in (Start, End):
            try:
                annotation.timeStart = datetime.strptime(Start, "%H:%M:%S.%f")
                annotation.timeEnd = datetime.strptime(End, "%H:%M:%S.%f")
            except:
                annotation.timeStart = datetime.strptime(Start, "%M:%S.%f")
                annotation.timeEnd = datetime.strptime(End, "%M:%S.%f")
        annotation.x = float(_Segment[0].get("x"))
        annotation.y = float(_Segment[0].get("y"))
        annotation.width = float(_Segment[0].get("w"))
        annotation.height = float(_Segment[0].get("h"))
        annotation.sx = float(_Segment[0].get("sx"))
        annotation.sy = float(_Segment[0].get("sy"))
        Appearance = each.find("appearance")
        if Appearance is not None:
            bgAlpha = Appearance.get("bgAlpha")
            bgColor = Appearance.get("bgColor")
            fgColor = Appearance.get("fgColor")
            textSize = Appearance.get("textSize")
        if bgAlpha is not None:
            annotation.bgOpacity = ConvertAlpha(bgAlpha)
        if bgAlpha is None:
            annotation.bgOpacity = DefaultTransparency()
        if bgColor is not None:
            annotation.bgColor = ConvertColor(bgColor)
        if bgColor is None:
            annotation.bgColor = White()
        if fgColor is not None:
            annotation.fgColor = ConvertColor(fgColor)
        if fgColor is None:
            annotation.fgColor = Black()
        if textSize is not None:
            annotation.textSize = float(textSize)
        if textSize is None:
            annotation.textSize = 3.15

        annotations.append(annotation)
    return annotations
