#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""转换器"""

import copy
import textwrap
from typing import List, Optional

from Annotations2Sub import Annotation
from Annotations2Sub.Sub import Draw, DrawCommand, Event, Tag
from Annotations2Sub.utils import Stderr, _


def Convert(
    annotations: List[Annotation],
    resolutionX: int = 100,
    resolutionY: int = 100,
) -> List[Event]:
    """转换 Annotations"""

    def ConvertAnnotation(each: Annotation) -> List[Event]:
        """将 Annotation 转换为 List[Event]"""

        # 致谢: https://github.com/nirbheek/youtube-ass &
        #       https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范

        def Text(event: Event) -> Event:
            """生成 Annotation 文本的 Event"""
            text = each.text

            # 模拟换行行为
            if "\n" not in text:
                length = int(width / (textSize / 2)) + 1
                text = "\n".join(
                    textwrap.wrap(text, width=length, drop_whitespace=False)
                )

            # 让前导空格生效
            if text.startswith(" "):
                text = "\u200b" + text

            # SSA 用 "\N" 换行
            text = text.replace("\n", r"\N")

            # 如果文本里包含大括号, 而且封闭, 会被识别为 "样式复写代码", 大括号内的文字不会显示
            # 而且仅 libass 支持大括号转义, xy-vsfilter 没有那玩意
            # 可以说, 本脚本(项目) 依赖于字幕滤镜(xy-vsfilter, libass)的怪癖
            text = text.replace("{", r"\{")
            text = text.replace("}", r"\}")

            variable_x = 1.0
            variable_y = 1.0

            if "transform_coefficient_x" in locals():
                variable_x = variable_x * transform_coefficient_x

            if "transform_coefficient_y" in locals():
                variable_y = variable_y * transform_coefficient_y

            # 文本与框保持一定距离
            _x = x + variable_x
            _y = y + variable_y

            # 为了可读性, 去掉多余的小数
            _x = round(_x, 3)
            _y = round(_y, 3)
            _textSize = round(textSize, 3)

            shadow = Tag.Shadow(0)
            tags = Tag()
            tags.extend(
                [
                    Tag.Align(7),
                    Tag.Pos(_x, _y),
                    Tag.Fontsize(_textSize),
                    Tag.PrimaryColour(each.fgColor),
                    Tag.Bord(0),
                    shadow,
                ]
            )
            if each.fontWeight == "bold":
                tags.append(Tag.Bold(1))
            if each.effects == "textdropshadow":
                shadow.shadow = 2

            event.Text = str(tags) + text
            return event

        def Box(event: Event) -> Event:
            """生成 Annotation 文本框的 Event"""

            _x = round(x, 3)
            _y = round(y, 3)
            _width = round(width, 3)
            _height = round(height, 3)

            tags = Tag()
            tags.extend(
                [
                    Tag.Align(7),
                    Tag.Pos(_x, _y),
                    Tag.PrimaryColour(each.bgColor),
                    Tag.PrimaryAlpha(each.bgOpacity),
                    Tag.Bord(0),
                    Tag.Shadow(0),
                ]
            )

            draws = Draw()
            draws.extend(
                [
                    DrawCommand(0, 0, "m"),
                    DrawCommand(_width, 0, "l"),
                    DrawCommand(_width, _height, "l"),
                    DrawCommand(0, _height, "l"),
                ]
            )
            # "绘图命令必须被包含在 {\p<等级>} 和 {\p0} 之间。"
            box_tag = r"{\p1}" + str(draws) + r"{\p0}"

            event.Text = str(tags) + box_tag
            return event

        def HighlightBox(event: Event) -> Event:
            variable1 = 1.0
            variable2 = 1.0

            if "transform_coefficient_x" in locals():
                variable1 = variable1 * transform_coefficient_x

            if "transform_coefficient_y" in locals():
                variable2 = variable2 * transform_coefficient_y

            x1 = x + variable1
            y1 = y + variable2
            x2 = x + width - variable1
            y2 = y + height - variable2

            _x = round(x, 3)
            _y = round(y, 3)
            x1 = round(x1, 3)
            y1 = round(y1, 3)
            x2 = round(x2, 3)
            y2 = round(y2, 3)
            _width = round(width, 3)
            _height = round(height, 3)

            tags = Tag()
            tags.extend(
                [
                    Tag.Align(7),
                    Tag.Pos(_x, _y),
                    Tag.PrimaryColour(each.bgColor),
                    Tag.PrimaryAlpha(each.bgOpacity),
                    Tag.Bord(0),
                    Tag.Shadow(0),
                    Tag.iClip(x1, y1, x2, y2),
                ]
            )

            draws = Draw()
            draws.extend(
                [
                    DrawCommand(0, 0, "m"),
                    DrawCommand(_width, 0, "l"),
                    DrawCommand(_width, _height, "l"),
                    DrawCommand(0, _height, "l"),
                ]
            )
            box_tag = r"{\p1}" + str(draws) + r"{\p0}"

            event.Text = str(tags) + box_tag
            return event

        def Triangle(event: Event) -> Optional[Event]:
            padding = 1.0

            # 坐标原点
            x_left = x - sx
            y_top = y - sy

            x_right = x_left + width
            y_bottom = y_top + height

            def draw(x1, y1, x2, y2):
                _sx = round(sx, 3)
                _sy = round(sy, 3)

                x1 = round(x1, 3)
                y1 = round(y1, 3)
                x2 = round(x2, 3)
                y2 = round(y2, 3)

                tags = Tag()
                tags.extend(
                    [
                        Tag.Align(7),
                        Tag.Pos(_sx, _sy),
                        Tag.PrimaryColour(each.bgColor),
                        Tag.PrimaryAlpha(each.bgOpacity),
                        Tag.Bord(0),
                        Tag.Shadow(0),
                    ]
                )

                draws = Draw()
                draws.extend(
                    [
                        DrawCommand(0, 0, "m"),
                        DrawCommand(x1, y1, "l"),
                        DrawCommand(x2, y2, "l"),
                    ]
                )
                box_tag = r"{\p1}" + str(draws) + r"{\p0}"

                event.Text = str(tags) + box_tag
                return event

            def up_down():
                x_start_multiplier = 0.174
                x_end_multiplier = 0.149

                x_start = width * x_start_multiplier
                x_end = width * x_end_multiplier

                x_left_1 = x_left + x_start
                x_left_2 = x_left_1 + x_end

                x_right_1 = x_right - x_end
                x_right_2 = x_right_1 - x_start

                is_top = y_top > padding
                is_bottom = y_bottom < padding
                is_keep_left = x_left >= width / 2
                is_keep_right = x_right <= width / 2

                x1 = y1 = x2 = y2 = None
                if is_top:
                    y2 = y1 = y_top
                if is_bottom:
                    y2 = y1 = y_bottom
                if is_keep_left:
                    x1 = x_left_1
                    x2 = x_left_2
                if is_keep_right:
                    x1 = x_right_1
                    x2 = x_right_2

                if None not in (x1, y1, x2, y2):
                    return draw(x1, y1, x2, y2)

            def left_right():
                y_start_multiplier = 0.12
                y_end_multiplier = 0.3

                y_start = height * y_start_multiplier
                y_end = height * y_end_multiplier

                y_middle_1 = y_top + y_start
                y_middle_2 = y_middle_1 + y_end

                is_left = x_left > padding
                is_right = x_right < padding

                x1 = x2 = None
                if is_left:
                    x2 = x1 = x_left
                if is_right:
                    x2 = x1 = x_right

                y1 = y_middle_1
                y2 = y_middle_2

                if None not in (x1, y1, x2, y2):
                    return draw(x1, y1, x2, y2)

            _event = up_down()
            if _event != None:
                return _event

            _event = left_right()
            if _event != None:
                return _event

            return None

        def popup_text() -> Event:
            _event = copy.copy(event)
            _event.Name += "popup_text;"

            return Text(_event)

        def popup_box() -> Event:
            _event = copy.copy(event)
            _event.Name = event.Name + "popup_box;"

            return Box(_event)

        def title() -> Event:
            _event = copy.copy(event)
            _event.Name += "title;"

            return Text(_event)

        def highlightText_text() -> Event:
            _event = copy.copy(event)
            _event.Name += "highlightText_text;"

            return Text(_event)

        def highlightText_box() -> Event:
            _event = copy.copy(event)
            _event.Name = event.Name + "highlightText_box;"

            return Box(_event)

        def speech_text() -> Event:
            _event = copy.copy(event)
            _event.Name += "speech_text;"

            return Text(_event)

        def speech_box() -> Event:
            _event = copy.copy(event)
            _event.Name += "speech_box;"

            return Box(_event)

        def speech_triangle() -> Optional[Event]:
            _event = copy.copy(event)
            _event.Name += "speech_triangle;"
            return Triangle(_event)

        def anchored_text() -> Event:
            _event = copy.copy(event)
            _event.Name += "anchored_text;"

            return Text(_event)

        def anchored_box() -> Event:
            _event = copy.copy(event)
            _event.Name += "anchored_box;"

            return Box(_event)

        def label_text() -> Event:
            _event = copy.copy(event)
            _event.Name += "label_text;"
            return Text(_event)

        def label_box() -> Event:
            _event = copy.copy(event)
            _event.Name += "label_box;"
            return Box(_event)

        def highlight_text() -> Event:
            _event = copy.copy(event)
            _event.Name += "highlight_text;"
            return Text(_event)

        def highlight_box() -> Event:
            _event = copy.copy(event)
            _event.Name += "highlight_box;"
            return HighlightBox(_event)

        def popup() -> List[Event]:
            return [popup_box(), popup_text()]

        def highlightText() -> List[Event]:
            return [highlightText_box(), highlightText_text()]

        def speech() -> List[Event]:
            events: List[Event] = []
            events.append(speech_box())
            _event = speech_triangle()
            if _event is not None:
                events.append(_event)
            events.append(speech_text())
            return events

        def anchored() -> List[Event]:
            return [anchored_box(), anchored_text()]

        def label() -> List[Event]:
            return [label_box(), label_text()]

        def highlight() -> List[Event]:
            return [highlight_box(), highlight_text()]

        event = Event()

        event.Start = each.timeStart
        event.End = each.timeEnd

        # Name 在 Aegisub 里是 "说话人"
        # 这里用于调试
        # author;id;function;alternative
        event.Name += each.author + ";"
        event.Name += each.id + ";"

        x = each.x
        y = each.y
        textSize = each.textSize
        width = each.width
        height = each.height
        sx = each.sx
        sy = each.sy

        if each.style == "title":
            textSize = textSize * 100 / 480

        if resolutionX != 100:
            transform_coefficient_x = resolutionX / 100

            def TransformX(x: float) -> float:
                return x * transform_coefficient_x

            x = TransformX(x)
            width = TransformX(width)
            sx = TransformX(sx)

        if resolutionY != 100:
            transform_coefficient_y = resolutionY / 100

            def TransformY(y: float) -> float:
                return y * transform_coefficient_y

            y = TransformY(y)
            textSize = TransformY(textSize)
            height = TransformY(height)
            sy = TransformY(sy)

        if each.style == "popup":
            return popup()
        elif each.style == "title":
            return [title()]
        elif each.style == "highlightText":
            return highlightText()
        elif each.style == "speech":
            return speech()
        elif each.style == "anchored":
            return anchored()
        elif each.style == "label":
            return label()
        elif each.style == "" and each.type == "highlight":
            return highlight()
        else:
            Stderr(_("不支持 {} 样式 ({})").format(each.style, each.id))
            return []

    events = []
    for each in annotations:
        events.extend(ConvertAnnotation(each))

    return events
