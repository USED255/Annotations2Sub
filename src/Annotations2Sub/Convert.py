#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""转换器"""

import copy
from typing import List

# 在重写本项目前, 我写了一些 Go 的代码
# 依照在 Go 中的经验把一个脚本拆成若干个模块
# 并上传到 PyPI
# 当然单文件脚本还是有用的
from Annotations2Sub.Annotation import Annotation
from Annotations2Sub.Color import Alpha, Color
from Annotations2Sub.Sub import Draw, DrawCommand, Event
from Annotations2Sub.utils import Stderr, _


def Convert(
    annotations: List[Annotation],
    libass: bool = False,
    resolutionX: int = 100,
    resolutionY: int = 100,
) -> List[Event]:
    """转换 Annotations"""

    def DumpColor(color: Color) -> str:
        """将 Color 转换为 SSA 的颜色表示"""
        return "&H{:02X}{:02X}{:02X}&".format(color.red, color.green, color.blue)

    def DumpAlpha(alpha: Alpha) -> str:
        """将 Alpha 转换为 SSA 的 Alpha 表示"""

        # 据 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 所说
        # SSA 的 Alpha 是透明度, 00 为不透明，FF 为全透明
        return "&H{:02X}&".format(255 - alpha.alpha)

    def ConvertAnnotation(each: Annotation) -> List[Event]:
        """将 Annotation 转换为 List[Event]"""

        # 致谢: https://github.com/nirbheek/youtube-ass &
        #       https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范

        def Text(event: Event) -> Event:
            """生成 Annotation 文本的 Event"""

            # Annotation 无非就是文本, 框, 或者是一个点击按钮和动图
            # 之前我用了一个函数生成标签, 还不如直接拼接
            tag = ""
            # 样式复写代码, 样式复写标签, ASS 标签, 特效标签, Aegisub 特效标签, 标签
            # 带引号的是从 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 粘过来的
            # "\an<位置>"
            # "<位置> 是一个数字，决定了字幕显示在屏幕上哪个位置。"
            # 默认 SSA 定位会定在文本中间
            # 用 \an7 指定在左上角.
            # "\pos(<x>,<y>)"
            # "将字幕定位在坐标点 <x>,<y>。"
            # SSA 和 Annotation 坐标系一致, y 向下(左手取向).
            # 这里坐标 +1 是为了美观, 与 Annotation 行为不一致
            tag += rf"\an7\pos({x + 1},{y + 1})"
            # "\fs<字体尺寸>"
            # "<字体尺寸> 是一个数字，指定了字体的点的尺寸。"
            # "注意，这里的字体尺寸并不是字号的大小，\fs20 并不是字体大小（font-size）为 20px，"
            # "而是指其行高（line-height）为 20px，主要归咎于 VSFilter 使用的 Windows GDI 的字体接口。"
            # 不明白字体大小和行高有什么区别
            tag += rf"\fs{str(textSize)}"
            # "\[<颜色序号>]c[&][H]<BBGGRR>[&]"
            # "<BBGGRR> 是一个十六进制的 RGB 值，但颜色顺序相反，前导的 0 可以省略。"
            # "<颜色序号> 可选值为 1、2、3 和 4，分别对应单独设置 PrimaryColour、SecondaryColour、OutlineColor 和 BackColour"
            # "其中的 & 和 H 按规范应该是要有的，但是如果没有也能正常解析。"
            # PrimaryColour 填充颜色, SecondaryColour 卡拉OK变色, OutlineColor 边框颜色, BackColour 阴影颜色
            tag += rf"\c{DumpColor(each.fgColor)}"
            # "\<颜色序号>a[&][H]<AA>[&]"
            # "<AA> 是一个十六进制的透明度数值，00 为全见，FF 为全透明。"
            # "<颜色序号> 含义同上，但这里不能省略。写法举例：\1a&H80&、\2a&H80、\3a80、\4a&H80&。"
            # "其中的 & 和 H 按规范应该是要有的，但是如果没有也能正常解析。"
            # Annotation 文本好像没有透明度, 这个很符合直觉
            tag += r"\2a&HFF&\3a&HFF&\4a&HFF&"
            # 现在加个括号就成了
            tag = "{" + tag + "}"
            # 直接拼接就可以了
            event.Text = tag + event.Text
            return event

        def Box(event: Event) -> Event:
            """生成 Annotation 文本框的 Event"""
            event.Layer = 0

            # 没什么太大的变化
            tag = ""
            tag += rf"\an7\pos({x},{y})"
            tag += rf"\c{DumpColor(each.bgColor)}"
            tag += rf"\1a{DumpAlpha(each.bgOpacity)}"
            tag += r"\2a&HFF&\3a&HFF&\4a&HFF&"
            tag = "{" + tag + "}"

            # 在之前这里我拼接字符串, 做的还没有全民核酸检测好
            # 现在画四个点直接闭合一个框
            d = Draw()
            d.Add(DrawCommand(0, 0, "m"))
            d.Add(DrawCommand(width, 0, "l"))
            d.Add(DrawCommand(width, height, "l"))
            d.Add(DrawCommand(0, height, "l"))
            box = d.Dump()
            # "绘图命令必须被包含在 {\p<等级>} 和 {\p0} 之间。"
            box_tag = r"{\p1}" + box + r"{\p0}"
            del box

            event.Text = tag + box_tag
            return event

        def popup_text(event: Event) -> Event:
            """生成 popup 样式的文本 Event"""

            # 多加几个字, 便于调试
            event.Name += "popup_text;"

            return Text(event)

        def popup_box(event: Event) -> Event:
            """生成 popup 样式的框 Event"""
            event.Name = event.Name + "popup_box;"

            return Box(event)

        def title(event: Event) -> Event:
            """生成 title 样式的 Event"""

            # 很明显 title 的字体大小和其他的不一样
            # 很像是我们熟悉的 "字体大小"
            # 但好像又不是
            # / 4 也是试出来的
            if resolutionX == 100 and resolutionY == 100:
                nonlocal textSize  # type: ignore
                textSize = round(textSize / 4, 3)

            event.Name += ";title"

            return Text(event)

        def highlightText_text(event: Event) -> Event:
            """生成 highlightText 样式的文本 Event"""
            event.Name += "highlightText_text;"

            return Text(event)

        def highlightText_box(event: Event) -> Event:
            """生成 highlightText 样式的框 Event"""
            event.Name = event.Name + "highlightText_box;"

            return Box(event)

        def speech_text(event: Event) -> Event:
            """生成 speech 样式的文本 Event"""
            event.Name += "speech_text;"

            return Text(event)

        def speech_box_1(event: Event) -> Event:
            """生成 speech 样式的框 Event"""
            event.Name += "speech_box_1;"

            return Box(event)

        def speech_box_2(event: Event) -> Event:
            """生成 speech 样式的第二个框 Event"""
            event.Name += "speech_box_2;"
            event.Layer = 0

            tag = ""
            tag += rf"\an7\pos({sx},{sy})"
            tag += rf"\c{DumpColor(each.bgColor)}"
            tag += rf"\1a{DumpAlpha(each.bgOpacity)}"
            tag += r"\2a&HFF&\3a&HFF&\4a&HFF&"
            tag = "{" + tag + "}"

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

            d = Draw()
            # 一共三个点, 怎么画都是个三角形
            d.Add(DrawCommand(0, 0, "m"))
            d.Add(DrawCommand(x1, y1, "l"))
            d.Add(DrawCommand(x2, y1, "l"))
            box = d.Dump()
            box_tag = r"{\p1}" + box + r"{\p0}"
            del box

            event.Text = tag + box_tag
            return event

        def anchored_text(event: Event) -> Event:
            """生成 anchored 样式的文本 Event"""
            event.Name += "anchored_text;"

            return Text(event)

        def anchored_box(event: Event) -> Event:
            """生成 anchored 样式的框 Event"""
            event.Name += "anchored_box;"

            return Box(event)

        def label_text(event: Event) -> Event:
            event.Name += "label_text;"
            return Text(event)

        def label_box(event: Event) -> Event:
            event.Name += "label_box;"
            return Box(event)

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

        text = each.text
        # SSA 用 "\N" 换行
        text = text.replace("\n", r"\N")
        if libass:
            # 如果文本里包含大括号, 而且封闭, 会被识别为 "样式复写代码", 大括号内的文字不会显示
            # 而且仅 libass 支持大括号转义, xy-vsfilter 没有那玩意
            # 可以说, 本脚本(项目) 依赖于字幕滤镜(xy-vsfilter, libass)的怪癖
            text = text.replace("{", r"\{")
            text = text.replace("}", r"\}")
        event.Text = text
        del text

        # 这里处理下数据供后面使用, 不需要处理都直接使用 each
        # Annotation 的定位是"百分比"
        # 恰好直接把"分辨率"设置为 100 就可以实现
        # 但是这其实还是依赖于字幕滤镜的怪癖
        transform_coefficient_x = resolutionX / 100
        transform_coefficient_y = resolutionY / 100
        # 浮点数太长了, 为了美观, 用 round 截断成三位, 字幕滤镜本身是支持小数的
        x = round(each.x * transform_coefficient_x, 3)
        y = round(each.y * transform_coefficient_y, 3)
        textSize = round(each.textSize * transform_coefficient_y, 3)
        width = round(each.width * transform_coefficient_x, 3)
        height = round(each.height * transform_coefficient_y, 3)
        sx = round(each.sx * transform_coefficient_x, 3)
        sy = round(each.sy * transform_coefficient_y, 3)

        if libass and resolutionX == 100 and resolutionY == 100:
            # 针对 libass 的 hack
            # 我也不知道 libass 咋回事
            # 1.776 是试出来的
            # 而且仅适用于 16:9 分辨率
            # 不要指望我在 libass 开 issue
            # 毕竟不知道还有多少脚本依赖于这个怪癖
            width = round(width * 1.776, 3)
            # sy 是中间变量, 不需要 round
            sy = sy * 1.776

        # Layer 是"层", 他们说大的会覆盖小的
        # 但是没有这个也可以正常显示, 之前就没有, 现在也就是安心些
        event.Layer = 1

        if each.style == "popup":
            # 用浅拷贝拷贝一遍再处理看起来简单些, 我不在意性能
            events.append(popup_text(copy.copy(event)))
            events.append(popup_box(copy.copy(event)))
        elif each.style == "title":
            events.append(title(copy.copy(event)))
        elif each.style == "highlightText":
            # 我还没遇到过 highlightText, 所以实现很可能不对
            events.append(highlightText_text(copy.copy(event)))
            events.append(highlightText_box(copy.copy(event)))
        elif each.style == "speech":
            # 上次恶心到我的地方, 这次想到了另一种方法处理掉了
            events.append(speech_text(copy.copy(event)))
            events.append(speech_box_1(copy.copy(event)))
            events.append(speech_box_2(copy.copy(event)))
            # 我没见过 "anchored" 实现不对
        elif each.style == "anchored":
            events.append(anchored_text(copy.copy(event)))
            events.append(anchored_box(copy.copy(event)))
        elif each.style == "label":
            events.append(label_text(copy.copy(event)))
            events.append(label_box(copy.copy(event)))
        else:
            # 传承于 Annotations2Sub™
            Stderr(_("不支持 {} 样式 ({})").format(each.style, each.id))

        return events

    events = []
    for each in annotations:
        # 一个 Annotations 可能会需要多个 Event 来表达.
        # each 这个习惯来源于 youtube-ass, 看起来比 i 要好一些
        events.extend(ConvertAnnotation(each))

    return events
