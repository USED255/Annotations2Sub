#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from typing import List

from Annotations2Sub.Annotation import Annotation
from Annotations2Sub.Color import Alpha, Color
from Annotations2Sub.Sub import Draw, Event, Point
from Annotations2Sub.internationalization import _
from Annotations2Sub.flag import Flags


def Convert(
    annotations: List[Annotation],
    libass: bool = False,
    resolutionX: int = 100,
    resolutionY: int = 100,
) -> List[Event]:
    """将 Annotation 列表转换为 Event 列表"""

    def ConvertColor(color: Color) -> str:
        return "&H{:02X}{:02X}{:02X}&".format(color.red, color.green, color.blue)

    def ConvertAlpha(alpha: Alpha) -> str:
        return "&H{:02X}&".format(alpha.alpha)

    def ConvertAnnotation(each: Annotation) -> List[Event]:
        # 致谢: https://github.com/nirbheek/youtube-ass
        # 致谢: https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
        def Text(event: Event) -> Event:
            tag = ""
            tag += r"\an7" + r"\pos({},{})".format(x + 1, y + 1)
            tag += r"\fs" + str(textSize)
            tag += r"\c" + fgColor
            tag += r"\2a" + "&HFF&" + r"\3a" + "&HFF&" + r"\4a" + "&HFF&"
            tag = "{" + tag + "}"

            event.Text = tag + event.Text
            return event

        def Box(event: Event) -> Event:
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

        def popup_text(event: Event) -> Event:
            event.Name += "_popup"

            return Text(event)

        def popup_box(event: Event) -> Event:
            event.Name = event.Name + "_popup_box"

            return Box(event)

        def title(event: Event) -> Event:
            # 很明显 title 字体大小是用 DPI 计算的
            nonlocal textSize  # type: ignore
            textSize = round(textSize / 4, 3)

            event.Name += "_title"

            return Text(event)

        def highlightText_text(event: Event) -> Event:
            event.Name += "_highlightText"

            return Text(event)

        def highlightText_box(event: Event) -> Event:
            event.Name = event.Name + "highlightText_box"

            return Box(event)

        def speech_text(event: Event) -> Event:
            event.Name += "_speech"

            return Text(event)

        def speech_box(event: Event) -> Event:
            event.Name += "_speech_box"
            event.Layer = 0

            tag = ""
            tag += r"\an7" + r"\pos({},{})".format(x, y)
            tag += r"\fs" + str(textSize)
            tag += r"\c" + bgColor
            tag += r"\1a" + bgOpacity
            tag += r"\2a" + "&HFF&" + r"\3a" + "&HFF&" + r"\4a" + "&HFF&"
            tag = "{" + tag + "}"

            d = Draw()
            d.Add(Point(0, 0, "m"))
            d.Add(Point(width, 0, "l"))
            d.Add(Point(width, height, "l"))
            d.Add(Point(0, height, "l"))

            """

    ┌────────────────────────────────────────────────►x
    │(0,0)
    │   ┌────────────────────────────────┬───────►
    │   │(x,y)                           │  height,0
    │   │0,0                             │
    │   │                    x3        x4│
    │   ├───────────────────x─────────x──┘  height,width
    │   │0,width             xx      x
    │   │                     xx    x
    │   │                       xx x
    │   │                        xx
    │   │                        (sx,sy)
    │   │                        sx1,sy2
    │   ▼
    ▼
    y

            """

            sx1 = sx - x
            sy1 = sy - y

            if sx < x + width / 2:
                x1 = width * 0.2
                x2 = width * 0.4
            elif sx > x + width / 2:
                x1 = width * 0.8
                x2 = width * 0.6
            else:
                x1 = width * 0.2
                x2 = width * 0.4

            if sy < y:
                y1 = float(0)
                x3 = min(x1, x2)
                x4 = max(x1, x2)
                d.draw.insert(1, Point(x3, y1, "l"))
                d.draw.insert(2, Point(sx1, sy1, "l"))
                d.draw.insert(3, Point(x4, y1, "l"))
            elif sy > y:
                y1 = height
                x3 = max(x1, x2)
                x4 = min(x1, x2)
                d.draw.insert(3, Point(x3, y1, "l"))
                d.draw.insert(4, Point(sx1, sy1, "l"))
                d.draw.insert(5, Point(x4, y1, "l"))
            else:
                y1 = 0
                x3 = min(x1, x2)
                x4 = max(x1, x2)
                d.draw.insert(1, Point(x3, y1, "l"))
                d.draw.insert(2, Point(sx1, sy1, "l"))
                d.draw.insert(3, Point(x4, y1, "l"))

            box = d.Dump()
            box = r"{\p1}" + box + r"{\p0}"

            event.Text = tag + box
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

        transformCoefficientX = resolutionX / 100
        transformCoefficientY = resolutionY / 100
        x = round(each.x * transformCoefficientX, 3)
        y = round(each.y * transformCoefficientY, 3)
        textSize = round(each.textSize * transformCoefficientY, 3)
        fgColor = ConvertColor(each.fgColor)
        bgColor = ConvertColor(each.bgColor)
        bgOpacity = ConvertAlpha(each.bgOpacity)
        width = round(each.width * transformCoefficientX, 3)
        height = round(each.height * transformCoefficientY, 3)
        sx = round(each.sx * transformCoefficientX, 3)
        sy = round(each.sy * transformCoefficientY, 3)

        if libass and resolutionX == 100 and resolutionY == 100:
            # 针对 libass 的 hack
            width = width * 1.776
            sy = sy * 1.776
        width = round(width, 3)

        event.Layer = 1

        if each.style == "popup":
            events.append(popup_text(copy.copy(event)))
            events.append(popup_box(copy.copy(event)))
        elif each.style == "title":
            events.append(title(copy.copy(event)))
        elif each.style == "highlightText" and Flags.unstable:
            events.append(highlightText_text(copy.copy(event)))
            events.append(highlightText_box(copy.copy(event)))
        elif each.style == "speech":
            events.append(speech_text(copy.copy(event)))
            events.append(speech_box(copy.copy(event)))
        else:
            print(_("不支持 {} 样式. ({})").format(each.style, each.id))

        return events

    events = []
    for each in annotations:
        events.extend(ConvertAnnotation(each))

    return events
