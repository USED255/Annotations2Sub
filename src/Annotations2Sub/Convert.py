#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""转换器"""

import copy
import textwrap
from typing import List

# 在重写本项目前, 我写了一些 Go 的代码
# 依照在 Go 中的经验把一个脚本拆成若干个模块
# 并上传到 PyPI
# 当然单文件脚本还是有用的
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

            if "\n" not in text:
                coefficient = 2.0
                if (
                    "transform_coefficient_x" not in locals()
                    or "transform_coefficient_y" not in locals()
                ):
                    coefficient = coefficient + 16 / 9
                length = int(width / (textSize / coefficient))

                line = []
                for _text in text.split("\n"):
                    line.extend(
                        textwrap.wrap(_text, width=length, drop_whitespace=False)
                    )
                text = "\n".join(line)

            if text.startswith(" "):
                # 让前导空格生效
                text = "\u200b" + text
            # SSA 用 "\N" 换行
            text = text.replace("\n", r"\N")
            # 如果文本里包含大括号, 而且封闭, 会被识别为 "样式复写代码", 大括号内的文字不会显示
            # 而且仅 libass 支持大括号转义, xy-vsfilter 没有那玩意
            # 可以说, 本脚本(项目) 依赖于字幕滤镜(xy-vsfilter, libass)的怪癖
            text = text.replace("{", r"\{")
            text = text.replace("}", r"\}")

            variable1 = 1.0
            variable2 = 1.0

            if "transform_coefficient_x" in locals():
                variable1 = variable1 * transform_coefficient_x

            if "transform_coefficient_y" in locals():
                variable2 = variable2 * transform_coefficient_y

            _x = x + variable1
            _y = y + variable2

            x1 = x + variable1
            y1 = y + variable2
            x2 = x + width - variable1
            y2 = y + height - variable2

            _x = round(_x, 3)
            _y = round(_y, 3)
            _textSize = round(textSize, 3)
            x1 = round(x1, 3)
            y1 = round(y1, 3)
            x2 = round(x2, 3)
            y2 = round(y2, 3)

            tags = Tag()
            tags.extend(
                [
                    Tag.Pos(_x, _y),
                    Tag.Fontsize(_textSize),
                    Tag.PrimaryColour(each.fgColor),
                    Tag.Bord(0),
                    Tag.Shadow(0),
                    Tag.Clip(x1, y1, x2, y2),
                ]
            )
            if each.fontWeight == "bold":
                tags.append(Tag.Bold(1))
            if each.effects == "textdropshadow":
                tags[4].shadow = 2

            event.Text = str(tags) + text
            return event

        def Box(event: Event) -> Event:
            """生成 Annotation 文本框的 Event"""

            _x = round(x, 3)
            _y = round(y, 3)
            _width = round(width, 3)
            _height = round(height, 3)

            # 在之前这里我拼接字符串, 做的还没有全民核酸检测好
            # 现在画四个点直接闭合一个框
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

            tags = Tag()
            tags.extend(
                [
                    Tag.Pos(_x, _y),
                    Tag.PrimaryColour(each.bgColor),
                    Tag.PrimaryAlpha(each.bgOpacity),
                    Tag.Bord(0),
                    Tag.Shadow(0),
                ]
            )
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

            # 在之前这里我拼接字符串, 做的还没有全民核酸检测好
            # 现在画四个点直接闭合一个框
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

            tags = Tag()
            tags.extend(
                [
                    Tag.Pos(_x, _y),
                    Tag.PrimaryColour(each.bgColor),
                    Tag.PrimaryAlpha(each.bgOpacity),
                    Tag.Bord(0),
                    Tag.Shadow(0),
                    Tag.iClip(x1, y1, x2, y2),
                ]
            )
            event.Text = str(tags) + box_tag
            return event

        def Triangle(event: Event) -> Event:
            # 开始只是按部就班的画一个气泡框
            # 之后我想可以拆成一个普通的方框和一个三角形
            # 这可以直接复用 Box, 气泡锚点定位也可以直接使用 /pos
            # 绘图变得更简单, 一共三个点

            # 图形定位在气泡锚点上, 图形需要画成一个三角形和 Box 拼接成一个气泡框
            # 原点是 (0,0), 那么如果锚点在框的下方点就应该往上画, 反之赤然

            # 以气泡锚点为原点求相对位置
            x1 = x - sx
            x2 = x - sx
            # 锚点靠那边就往那边画
            if sx < x + width / 2:
                x1 = x1 + width * 0.2
                x2 = x2 + width * 0.4
            else:
                x1 = x1 + width * 0.8
                x2 = x2 + width * 0.6

            # 以气泡锚点为原点求相对位置
            y1 = y - sy
            # 如果锚点在框的下方那么三角的边接的是框的下边, 所以是 y1 + height
            if sy > y:
                y1 = y1 + height

            x1 = round(x1, 3)
            y1 = round(y1, 3)
            x2 = round(x2, 3)

            draws = Draw()
            # 一共三个点, 怎么画都是个三角形
            draws.extend(
                [
                    DrawCommand(0, 0, "m"),
                    DrawCommand(x1, y1, "l"),
                    DrawCommand(x2, y1, "l"),
                ]
            )
            box = str(draws)
            box_tag = r"{\p1}" + box + r"{\p0}"
            del box
            _sx = sx
            _sy = sy
            _sx = round(_sx, 3)
            _sy = round(_sy, 3)
            tags = Tag()
            tags.extend(
                [
                    Tag.Pos(_sx, _sy),
                    Tag.PrimaryColour(each.bgColor),
                    Tag.PrimaryAlpha(each.bgOpacity),
                    Tag.Bord(0),
                    Tag.Shadow(0),
                ]
            )
            event.Text = str(tags) + box_tag
            return event

        def Triangle2(event: Event) -> Event:
            h_base_start_multiplier = 0.17379070765180116
            h_base_end_multiplier = 0.14896346370154384
            v_base_start_multiplier = 0.12
            v_base_end_multiplier = 0.3

            h_s_v = width * h_base_start_multiplier
            h_e_v = width * h_base_end_multiplier
            v_s_v = height * v_base_start_multiplier
            v_e_v = height * v_base_end_multiplier

            x1 = x - sx
            y1 = y - sy

            v1 = x1 + h_s_v
            v2 = x1 + h_s_v * 2
            v3 = y1 + height
            v4 = y1 + v_s_v

            def f(event, x1, y1, x2):
                x1 = round(x1, 3)
                y1 = round(y1, 3)
                x2 = round(x2, 3)
                _sx = round(sx, 3)
                _sy = round(sy, 3)

                draws = Draw()
                draws.extend(
                    [
                        DrawCommand(0, 0, "m"),
                        DrawCommand(x1, y1, "l"),
                        DrawCommand(x2, y1, "l"),
                    ]
                )
                box_tag = r"{\p1}" + str(draws) + r"{\p0}"

                tags = Tag()
                tags.extend(
                    [
                        Tag.Pos(_sx, _sy),
                        Tag.PrimaryColour(each.bgColor),
                        Tag.PrimaryAlpha(each.bgOpacity),
                        Tag.Bord(0),
                        Tag.Shadow(0),
                    ]
                )
                event.Text = str(tags) + box_tag
                return event

            def f2(event, x1, y1, y2):
                x1 = round(x1, 3)
                y1 = round(y1, 3)
                y2 = round(y2, 3)
                _sx = round(sx, 3)
                _sy = round(sy, 3)

                draws = Draw()
                draws.extend(
                    [
                        DrawCommand(0, 0, "m"),
                        DrawCommand(x1, y1, "l"),
                        DrawCommand(y2, y1, "l"),
                    ]
                )
                box_tag = r"{\p1}" + str(draws) + r"{\p0}"

                tags = Tag()
                tags.extend(
                    [
                        Tag.Pos(_sx, _sy),
                        Tag.PrimaryColour(each.bgColor),
                        Tag.PrimaryAlpha(each.bgOpacity),
                        Tag.Bord(0),
                        Tag.Shadow(0),
                    ]
                )
                event.Text = str(tags) + box_tag
                return event

            def top_left():
                _x1 = v1
                x2 = _x1 + h_e_v

                return f(event, _x1, y1, x2)

            def top_right():
                _x1 = v2
                x2 = _x1 - h_e_v

                return f(event, _x1, y1, x2)

            def bottom_left():
                _x1 = v1
                x2 = _x1 + h_e_v

                return f(event, _x1, v3, x2)

            def bottom_right():
                _x1 = v2
                x2 = _x1 - h_e_v

                return f(event, _x1, v3, x2)

            def left():
                _y1 = v4
                y2 = _y1 + v_e_v
                return f2(event, x1, _y1, y2)

            def right():
                _y1 = v4
                y2 = _y1 + v_e_v

                _x1 = x1 + width
                return f2(event, _x1, _y1, y2)

            direction_padding = 20
            bottom = False
            top = False
            _right = False
            _left = False

            if sy < (y - direction_padding):
                top = True
            if sy > y + height:
                bottom = True

            if sx < ((x + width) - (width / 2)):
                _left = True
            if sx > ((x + width) - (width / 2)):
                _right = True

            if (
                sx > (x + width)
                and sy > (y - direction_padding)
                and sy < ((y + height) - direction_padding)
            ):
                return right()
            if sx < x and sy > y and sy < (y + height):
                return left()

            if top and _left:
                return top_left()
            if top and _right:
                return top_right()
            if bottom and _left:
                return bottom_left()
            if bottom and _right:
                return bottom_right()

            return bottom_left()

        def popup_text() -> Event:
            """生成 popup 样式的文本 Event"""
            _event = copy.copy(event)
            # 多加几个字, 便于调试
            _event.Name += "popup_text;"

            return Text(_event)

        def popup_box() -> Event:
            """生成 popup 样式的框 Event"""
            _event = copy.copy(event)
            _event.Name = event.Name + "popup_box;"

            return Box(_event)

        def title() -> Event:
            """生成 title 样式的 Event"""
            _event = copy.copy(event)
            _event.Name += ";title"

            return Text(_event)

        def highlightText_text() -> Event:
            """生成 highlightText 样式的文本 Event"""
            _event = copy.copy(event)
            _event.Name += "highlightText_text;"

            return Text(_event)

        def highlightText_box() -> Event:
            """生成 highlightText 样式的框 Event"""
            _event = copy.copy(event)
            _event.Name = event.Name + "highlightText_box;"

            return Box(_event)

        def speech_text() -> Event:
            """生成 speech 样式的文本 Event"""
            _event = copy.copy(event)
            _event.Name += "speech_text;"

            return Text(_event)

        def speech_box() -> Event:
            """生成 speech 样式的框 Event"""
            _event = copy.copy(event)
            _event.Name += "speech_box;"

            return Box(_event)

        def speech_triangle() -> Event:
            _event = copy.copy(event)
            _event.Name += "speech_triangle;"
            return Triangle(_event)

        def anchored_text() -> Event:
            """生成 anchored 样式的文本 Event"""
            _event = copy.copy(event)
            _event.Name += "anchored_text;"

            return Text(_event)

        def anchored_box() -> Event:
            _event = copy.copy(event)
            """生成 anchored 样式的框 Event"""
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

        events: List[Event] = []
        event = Event()

        # 我把 Annotation 抽成单独的结构就是为了这种效果
        # 直接赋值, 不用加上一大坨清洗代码
        event.Start = each.timeStart
        event.End = each.timeEnd
        # author;id;function;alternative
        # Name 在 Aegisub 里是 "说话人"
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
            # Windows 酱赛高
            textSize = textSize * 100 / 480

        if resolutionX != 100:
            # Annotations 的定位是"百分比"
            # 恰好直接把"分辨率"设置为 100 就可以实现
            # 但是这其实还是依赖于字幕滤镜的怪癖
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

        # 破坏性更改: 移除 --embrace-libass(b6e7cde)
        # 在 https://github.com/libass/libass/pull/645 之前
        # libass 的 x和y轴共用了一个缩放系数
        # 以至于我需要将 width * 1.776 手动修正缩放错误
        # 1.776 = 16/9 😅

        if each.style == "popup":
            # 用浅拷贝拷贝一遍再处理看起来简单些, 我不在意性能
            events.append(popup_box())
            events.append(popup_text())
        elif each.style == "title":
            events.append(title())
        elif each.style == "highlightText":
            # 我没见过 highlightText, 所以实现很可能不对
            events.append(highlightText_box())
            events.append(highlightText_text())
        elif each.style == "speech":
            events.append(speech_box())
            events.append(speech_triangle())
            events.append(speech_text())
            # 我没见过 "anchored" 所有实现很可能不对
        elif each.style == "anchored":
            events.append(anchored_box())
            events.append(anchored_text())
        elif each.style == "label":
            events.append(label_box())
            events.append(label_text())
        elif each.style == "" and each.type == "highlight":
            events.append(highlight_box())
            events.append(highlight_text())
        else:
            Stderr(_("不支持 {} 样式 ({})").format(each.style, each.id))

        return events

    events = []
    for each in annotations:
        # 一个 Annotation 可能会需要多个 Event 来表达.
        events.extend(ConvertAnnotation(each))

    return events
