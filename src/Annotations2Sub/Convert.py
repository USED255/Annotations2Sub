#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import gettext
from typing import List, Optional
from xml.etree.ElementTree import Element

from Annotations2Sub.Annotation import Annotation
from Annotations2Sub.Color import Alpha, Color
from Annotations2Sub.Sub import Draw, Event, Point

# translate = gettext.translation("Annotations2Sub", "translations")
# _ = translate.gettext
_ = gettext.gettext


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
            print(_("本脚本暂不支持{}类型. ()").format(type, annotation.id))
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


def Convert(annotations: List[Annotation], libass: bool = False) -> List[Event]:
    """将 Annotation 列表转换为 Event 列表"""

    def ConvertColor(color: Color) -> str:
        return "&H{:02X}{:02X}{:02X}&".format(color.red, color.green, color.blue)

    def ConvertAlpha(alpha: Alpha) -> str:
        return "&H{:02X}&".format(alpha.alpha)

    def ConvertAnnotation(each: Annotation) -> List[Event]:
        # 致谢: https://github.com/nirbheek/youtube-ass
        # 致谢: https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
        def popup():
            nonlocal event
            x = round(each.x, 3)
            y = round(each.y, 3)
            textSize = round(each.textSize, 3)
            fgColor = ConvertColor(each.fgColor)
            bgColor = ConvertColor(each.bgColor)
            bgOpacity = ConvertAlpha(each.bgOpacity)
            width = round(each.width)
            height = round(each.height)

            if libass:
                # 针对 libass 的 hack
                width = width * 1.776
            width = round(width, 3)
            event.Name += "_popup"

            tag = ""
            tag += r"\an7" + r"\pos({},{})".format(x + 1, y + 1)
            tag += r"\fs{}".format(textSize)
            tag += r"\c" + fgColor
            tag += r"\2a" + "&HFF&" + r"\3a" + "&HFF&" + r"\4a" + "&HFF&"
            tag = "{" + tag + "}"
            event.Text = tag + event.Text
            events.append(event)

            event = copy.copy(event)

            d = Draw()
            d.Add(Point(0, 0, "m"))
            d.Add(Point(width, 0, "l"))
            d.Add(Point(width, height, "l"))
            d.Add(Point(0, height, "l"))
            d_str = d.Dump()
            box = r"{\p1}" + d_str + r"{\p0}"

            tag = ""
            tag += r"\an7" + r"\pos({},{})".format(x, y)
            tag += r"\fs{}".format(textSize)
            tag += r"\c" + bgColor
            tag += r"\1a" + bgOpacity
            tag += r"\2a" + "&HFF&" + r"\3a" + "&HFF&" + r"\4a" + "&HFF&"
            tag = "{" + tag + "}"

            event.Text = tag + box
            event.Name = event.Name + "_box"
            events.append(event)

        def title():
            nonlocal event
            x = round(each.x, 3)
            y = round(each.y, 3)
            # 很明显 title 字体大小是用 DPI 72 计算的
            textSize = round(each.textSize / 4, 3)
            fgColor = ConvertColor(each.fgColor)
            bgOpacity = ConvertAlpha(each.bgOpacity)

            event.Name += "_title"
            tag = ""
            tag += r"\an7" + r"\pos({},{})".format(x, y)
            tag += r"\fs{}".format(textSize)
            tag += r"\c" + fgColor
            tag += r"\1a" + bgOpacity
            #tag += r"\b1"
            tag += r"\2a" + "&HFF&" + r"\3a" + "&HFF&" + r"\4a" + "&HFF&"
            tag = "{" + tag + "}"

            event.Text = tag + event.Text
            events.append(event)

        events: List[Event] = []
        event = Event()

        event.Start = each.timeStart
        event.End = each.timeEnd
        event.Name = each.id

        text = each.text
        text = text.replace("\n", r"\N")
        if libass:
            # 仅 libass 支持大括号转义
            text = text.replace(r"{", r"\{")
            text = text.replace(r"}", r"\}")
        event.Text = text

        if each.style == "popup":
            popup()
        elif each.style == "title":
            title()
        else:
            print(_("本脚本暂不支持 {} 样式. ({})").format(each.style, each.id))

        return events

    events = []
    for each in annotations:
        events.extend(ConvertAnnotation(each))

    return events
