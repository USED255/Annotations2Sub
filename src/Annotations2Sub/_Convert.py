# -*- coding: utf-8 -*-

"""转换器"""

import copy
import textwrap
from typing import List, Optional

from Annotations2Sub._Sub import Draw, DrawCommand, Event, Tag
from Annotations2Sub.Annotations import Annotation
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

        def Warp(text: str, length: int) -> str:
            def wrap(text: str) -> str:
                return "\n".join(
                    textwrap.wrap(text, width=length, drop_whitespace=False)
                )

            _text = ""
            lines = text.split("\n")

            for line in lines[:-1]:
                _text += wrap(line) + "\n"
            _text += wrap(lines[-1])

            return _text

        def Text(event: Event) -> Event:
            """生成 Annotation 文本的 Event"""

            # 文本与框保持一定距离
            nonlocal x
            nonlocal y

            x = x + padding_x
            y = y + padding_y

            tags = Tag()
            tags.extend(
                [
                    Tag.Align(7),
                    Tag.Pos(x, y),
                    Tag.Fontsize(textSize),
                    Tag.PrimaryColour(each.fgColor),
                    Tag.Bord(0),
                    Tag.Shadow(0),
                ]
            )
            if each.fontWeight == "bold":
                tags.append(Tag.Bold(1))

            event.Text = str(tags) + text
            return event

        def CenterText(event: Event) -> Event:
            # 相比 Text, 文字会居中

            # 模拟居中
            nonlocal x
            nonlocal y

            x = x + (width / 2)
            y = y + (height / 2)

            shadow = Tag.Shadow(0)
            tags = Tag()
            tags.extend(
                [
                    Tag.Align(5),
                    Tag.Pos(x, y),
                    Tag.Fontsize(textSize),
                    Tag.PrimaryColour(each.fgColor),
                    Tag.Bord(0),
                    shadow,
                ]
            )
            if each.fontWeight == "bold":
                tags.append(Tag.Bold(1))

            event.Text = str(tags) + text
            return event

        def Box(event: Event) -> Event:
            """生成 Annotation 文本框的 Event"""

            tags = Tag()
            tags.extend(
                [
                    Tag.Align(7),
                    Tag.Pos(x, y),
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
                    DrawCommand(width, 0, "l"),
                    DrawCommand(width, height, "l"),
                    DrawCommand(0, height, "l"),
                ]
            )
            # "绘图命令必须被包含在 {\p<等级>} 和 {\p0} 之间。"
            box_tag = r"{\p1}" + str(draws) + r"{\p0}"

            event.Text = str(tags) + box_tag
            return event

        def HollowBox(event: Event) -> Event:
            nonlocal padding_x
            nonlocal padding_y

            padding_x = padding_x * 0.2
            padding_y = padding_y * 0.2

            x1 = x + padding_x
            y1 = y + padding_y
            x2 = x + width - padding_x
            y2 = y + height - padding_y

            tags = Tag()
            tags.extend(
                [
                    Tag.Align(7),
                    Tag.Pos(x, y),
                    Tag.PrimaryColour(each.bgColor),
                    Tag.PrimaryAlpha(each.bgOpacity),
                    Tag.Bord(0),
                    Tag.Shadow(0),
                    # 将一个框挖空模拟其效果
                    Tag.iClip(x1, y1, x2, y2),
                ]
            )

            draws = Draw()
            draws.extend(
                [
                    DrawCommand(0, 0, "m"),
                    DrawCommand(width, 0, "l"),
                    DrawCommand(width, height, "l"),
                    DrawCommand(0, height, "l"),
                ]
            )
            box_tag = r"{\p1}" + str(draws) + r"{\p0}"

            event.Text = str(tags) + box_tag
            return event

        def Triangle(event: Event) -> Optional[Event]:
            # 气泡框的框和柄分开绘制
            # 这个函数绘制气泡柄
            padding = padding_y

            # 坐标原点
            x_left = x - sx
            y_top = y - sy

            x_right = x_left + width
            y_bottom = y_top + height

            def draw(x1, y1, x2, y2):

                tags = Tag()
                tags.extend(
                    [
                        Tag.Align(7),
                        Tag.Pos(sx, sy),
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

            return CenterText(_event)

        def highlightText_text() -> Event:
            _event = copy.copy(event)
            _event.Name += "highlightText_text;"

            return CenterText(_event)

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

        def anchored_triangle() -> Optional[Event]:
            _event = copy.copy(event)
            _event.Name += "anchored_triangle;"
            return Triangle(_event)

        def label_text() -> Event:
            _event = copy.copy(event)
            _event.Name += "label_text;"
            return Text(_event)

        def label_box() -> Event:
            _event = copy.copy(event)
            _event.Name += "label_box;"
            return Box(_event)

        def label_hollow_box() -> Event:
            _event = copy.copy(event)
            _event.Name += "label_hollow_box;"
            return HollowBox(_event)

        def highlight_text() -> Event:
            _event = copy.copy(event)
            _event.Name += "highlight_text;"
            return Text(_event)

        def highlight_box() -> Event:
            _event = copy.copy(event)
            _event.Name += "highlight_box;"
            return HollowBox(_event)

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
            events: List[Event] = []
            events.append(anchored_box())
            _event = anchored_triangle()
            if _event is not None:
                events.append(_event)
            events.append(anchored_text())
            return events

        def label() -> List[Event]:
            events: List[Event] = []
            events.append(label_hollow_box())

            line_count = text.count("\n") + 1

            nonlocal y
            nonlocal height

            v1 = height - textSize * line_count
            v1 = v1 - padding_y * 2
            y = y + v1
            height = height - v1

            events.append(label_box())
            events.append(label_text())
            return events

        def highlight() -> List[Event]:
            return [highlight_box(), highlight_text()]

        # 框与文本之间有填充距离
        padding_x = 1.0
        padding_y = 1.0

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
        text = each.text

        # 钳制字体大小
        line_count = text.count("\n") + 1

        _height = height - padding_y * (1 + line_count)
        if _height <= 0:
            _height = height

        Max_textSize = _height / line_count
        if textSize > Max_textSize:
            textSize = Max_textSize

        # 模拟换行
        if textSize == 0:
            textSize = 3.5

        length = int(width / (textSize / 4)) + 1
        text = Warp(text, length)

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

        textSize = textSize * 1.12

        if resolutionX != 100:
            transform_coefficient_x = resolutionX / 100

            def TransformX(x: float) -> float:
                return x * transform_coefficient_x

            x = TransformX(x)
            width = TransformX(width)
            sx = TransformX(sx)
            padding_x = TransformX(padding_x)

        if resolutionY != 100:
            transform_coefficient_y = resolutionY / 100

            def TransformY(y: float) -> float:
                return y * transform_coefficient_y

            y = TransformY(y)
            textSize = TransformY(textSize)
            height = TransformY(height)
            sy = TransformY(sy)
            padding_y = TransformY(padding_y)

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
            Stderr(_('不支持 "{}" 样式 ({})').format(each.style, each.id))
            return []

    patch: dict[str, dict] = {}
    events = []

    for each in annotations:
        if each.ref != "":
            patch[each.ref] = {}

    for each in annotations:
        if each.id in patch:
            patch[each.id] = {"timeStart": each.timeStart, "timeEnd": each.timeEnd}

    for each in annotations:
        if each.ref in patch:
            each.timeStart = patch[each.ref]["timeStart"]
            each.timeEnd = patch[each.ref]["timeEnd"]

    for each in annotations:
        events.extend(ConvertAnnotation(each))

    return events
