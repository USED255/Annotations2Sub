# -*- coding: utf-8 -*-

"""转换器"""

import copy
import textwrap
from typing import Dict, List, Optional

from Annotations2Sub._Sub import Draw, DrawCommand, Event, Tag
from Annotations2Sub.Annotations import Annotation
from Annotations2Sub.utils import Stderr, _


def Convert(
    annotations: List[Annotation],
    resolutionX: int = 100,
    resolutionY: int = 100,
) -> List[Event]:
    """转换 Annotations"""
    """
┌────────────────┐   ┌───────┐                           
│List[Annotation]│ ┌►│popup()│                           
└───────┬────────┘ │ └┬┬─────┘                           
        ▼          │  ││ ┌────────────┐  ┌─────┐         
 ┌─────────────┐   │  │└►│ popup_box()├─►│Box()├──┐      
 │Preprocessing│   │  │  └────────────┘  └─────┘  │      
 └──────┬──────┘   │  │  ┌────────────┐  ┌──────┐ │      
        ▼          │  └─►│popup_text()├─►│Text()├─┤      
  ┌──────────┐     │     └────────────┘  └──────┘ ▼      
  │Processing├─────┤ ┌───────┐              ┌───────────┐
  └──────────┘     ├►│title()│              │List[Event]│
                   │ └─┬─────┘              └───────────┘
                   │   │ ┌────────────┐           ▲      
                   │   └►│CenterText()├───────────┤      
                   │     └────────────┘           │      
                   │ ┌────┐  ┌────┐               │      
                   └►│... ├─►│... ├───────────────┘      
                     └────┘  └────┘                      
    """

    def ConvertAnnotation(each: Annotation) -> List[Event]:

        # 致谢: https://github.com/nirbheek/youtube-ass &
        #       https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范

        def Wrap(text: str, length: int) -> str:
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
            # 文本与框保持一定距离

            _x = x + padding_x
            _y = y + padding_y
            #

            tags = Tag()
            tags.extend(
                [
                    Tag.Align(7),
                    Tag.Pos(_x, _y),
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
            _x = x + (width / 2)
            _y = y + (height / 2)
            #

            shadow = Tag.Shadow(0)
            tags = Tag()
            tags.extend(
                [
                    Tag.Align(5),
                    Tag.Pos(_x, _y),
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
            _padding_x = padding_x
            _padding_y = padding_y

            if resolutionX > resolutionY:
                ratio = resolutionX / resolutionY
                _padding_y = _padding_y * ratio

            if resolutionY > resolutionX:
                ratio = resolutionY / resolutionX
                _padding_x = _padding_x * ratio

            _padding_x = _padding_x * 0.3
            _padding_y = _padding_y * 0.3

            x1 = x + _padding_x
            y1 = y + _padding_y
            x2 = x + width - _padding_x
            y2 = y + height - _padding_y

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
            # 致谢: https://github.com/po5/assnotations

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

            line_count = text.count(r"\N") + 1
            _height = textSize * line_count

            # 需要修改之后的值以便模拟其效果,
            # Text 和 Box 也被其他函数使用因此不能用新变量,
            # 函数返回后没有其他过程, 因此不会有污染.
            nonlocal y  # type: ignore
            nonlocal height  # type: ignore

            y = y + height - _height - padding_y * 2
            height = _height + padding_y * 2

            events.append(label_box())
            events.append(label_text())
            return events

        def highlight() -> List[Event]:
            return [highlight_box(), highlight_text()]

        x = each.x
        y = each.y
        textSize = each.textSize
        width = each.width
        height = each.height
        sx = each.sx
        sy = each.sy
        text = each.text

        # 框与文本之间有填充距离
        padding_x = 1.0
        padding_y = 1.0

        # 自适应文本
        # 参考 https://github.com/USED255/youtube_annotations_hack/blob/50db2b95133ddb0283ce6adb2ccadc11510caf27/web/yts/jsbin/player-vflpusdz-/en_US/annotations_module.js#L2509
        _text = text
        if textSize == 0:
            textSize = 0.5

        def length_overflows() -> bool:
            line_count = _text.count("\n") + 1
            return textSize * 1.12 * line_count > height - padding_y * 2

        def width_overflows() -> bool:
            l = []
            for line in _text.split("\n"):
                l.append(len(line) * (textSize / 4))
            return max(l) > width

        if length_overflows() or width_overflows():
            min_font_size = 0.5
            max_font_size = textSize
            step = textSize
            while True:
                step = step / 2

                if step < 0.1:
                    break

                if length_overflows():
                    textSize = max(textSize - step, min_font_size)
                else:
                    textSize = min(textSize + step, max_font_size)

                _width = width - padding_x * 2
                if _width < 0:
                    _width = width
                length = int(_width / (textSize / 4)) + 1
                _text = Wrap(text, length)

        text = _text
        #

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

        event = Event()

        event.Start = each.timeStart
        event.End = each.timeEnd

        # Name 在 Aegisub 里是 "说话人"
        # 这里用于调试
        # author;id;function;alternative
        event.Name += each.author + ";"
        event.Name += each.id + ";"

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

    #      Dict[Ref:str, Dict[timeStart:datetime, timeEnd:datetime]]
    patch: Dict[str, Dict] = {}
    events = []

    for each in annotations:
        if each.ref != "":
            patch[each.ref] = {}

    for each in annotations:
        if each.id in patch:
            patch[each.id] = {"timeStart": each.timeStart, "timeEnd": each.timeEnd}

    for each in annotations:
        if each.ref in patch:
            if patch[each.ref] == {}:
                continue
            each.timeStart = patch[each.ref]["timeStart"]
            each.timeEnd = patch[each.ref]["timeEnd"]

    for each in annotations:
        events.extend(ConvertAnnotation(each))

    return events
