#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from typing import List

from Annotations2Sub.Annotation import Annotation
from Annotations2Sub.Color import Alpha, Color
from Annotations2Sub.Sub import Draw, Event, Point

import gettext
import os

translate = gettext.translation(
    "Annotations2Sub",
    os.path.join(os.path.split(os.path.realpath(__file__))[0], "locales"),
)
_ = translate.gettext


def Convert(annotations: List[Annotation], libass: bool = False) -> List[Event]:
    """将 Annotation 列表转换为 Event 列表"""

    def ConvertColor(color: Color) -> str:
        return "&H{:02X}{:02X}{:02X}&".format(color.red, color.green, color.blue)

    def ConvertAlpha(alpha: Alpha) -> str:
        return "&H{:02X}&".format(alpha.alpha)

    def ConvertAnnotation(each: Annotation) -> List[Event]:
        # 致谢: https://github.com/nirbheek/youtube-ass
        # 致谢: https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
        def popup(event: Event) -> Event:
            event.Name += "_popup"

            tag = ""
            tag += r"\an7" + r"\pos({},{})".format(x + 1, y + 1)
            tag += r"\fs" + str(textSize)
            tag += r"\c" + fgColor
            tag += r"\2a" + "&HFF&" + r"\3a" + "&HFF&" + r"\4a" + "&HFF&"
            tag = "{" + tag + "}"

            event.Text = tag + event.Text
            return event

        def popup_box(event: Event) -> Event:
            event.Name = event.Name + "_popup_box"
            event.Layer = 0

            d = Draw()
            d.Add(Point(0, 0, "m"))
            d.Add(Point(width, 0, "l"))
            d.Add(Point(width, height, "l"))
            d.Add(Point(0, height, "l"))
            box = d.Dump()
            box = r"{\p1}" + box + r"{\p0}"

            tag = ""
            tag += r"\an7" + r"\pos({},{})".format(x, y)
            tag += r"\fs" + str(textSize)
            tag += r"\c" + bgColor
            tag += r"\1a" + bgOpacity
            tag += r"\2a" + "&HFF&" + r"\3a" + "&HFF&" + r"\4a" + "&HFF&"
            tag = "{" + tag + "}"

            event.Text = tag + box
            return event

        def title(event: Event) -> Event:
            # 很明显 title 字体大小是用 DPI 72 计算的
            textSize = round(each.textSize / 4, 3)

            event.Name += "_title"

            tag = ""
            tag += r"\an7" + r"\pos({},{})".format(x, y)
            tag += r"\fs" + str(textSize)
            tag += r"\c" + fgColor
            tag += r"\b500"
            tag += r"\2a" + "&HFF&" + r"\3a" + "&HFF&" + r"\4a" + "&HFF&"
            tag = "{" + tag + "}"

            event.Text = tag + event.Text
            return event

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

        x = round(each.x, 3)
        y = round(each.y, 3)
        textSize = round(each.textSize, 3)
        fgColor = ConvertColor(each.fgColor)
        bgColor = ConvertColor(each.bgColor)
        bgOpacity = ConvertAlpha(each.bgOpacity)
        width = round(each.width, 3)
        height = round(each.height, 3)

        if libass:
            # 针对 libass 的 hack
            width = width * 1.776
        width = round(width, 3)

        event.Layer = 1

        if each.style == "popup":
            events.append(popup(copy.copy(event)))
            events.append(popup_box(copy.copy(event)))
        elif each.style == "title":
            events.append(title(copy.copy(event)))
        else:
            print(_("本脚本暂不支持 {} 样式. ({})").format(each.style, each.id))

        return events

    events = []
    for each in annotations:
        events.extend(ConvertAnnotation(each))

    return events
