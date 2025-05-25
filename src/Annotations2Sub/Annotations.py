# -*- coding: utf-8 -*-
"""管理 YouTube 注释数据的解析和表示。

此模块定义了 `Annotation` 类，该类封装了单个 YouTube 注释的属性
（例如文本、时间、位置、样式）。
它提供了 `Parse` 函数，用于将 XML 元素树（通常来自 `annotations.xml` 文件）
转换为 `Annotation` 对象列表。
还包括对无效注释文档的错误处理。
"""

"""Annotations 相关"""

import datetime as dt
import math
from datetime import datetime
from typing import List, Optional, Union
from xml.etree.ElementTree import Element

from Annotations2Sub.Color import Alpha, Color
from Annotations2Sub.i18n import _
from Annotations2Sub.utils import Info, Stderr

# 兼容 Python3.6, 3.7
# Python3.6, 3.7 的 typing 没有 Literal
try:
    from typing import Literal
except ImportError:
    pass


class NotAnnotationsDocumentError(ValueError):
    """当 XML 文档不是有效的 YouTube 注释文件时引发的自定义异常。

    这通常意味着根“document”元素丢失，或者未找到“annotations”子元素，
    表明输入 XML 不符合 YouTube 注释数据的预期结构。
    """
    pass


class Annotation:
    """代表单个 YouTube 视频注释。

    此类存储单个注释的所有相关信息，例如其类型、文本内容、时间、
    位置、样式属性（颜色、字体大小）以及关联的作者。
    它旨在捕获 YouTube 定义的注释的基本属性。

    属性:
        id: 注释的唯一标识符。
        type: 注释的类型 (例如 "text", "highlight")。
        style: 注释的视觉样式 (例如 "popup", "title", "speech")。
        author: 注释的作者 (通常是频道 ID)。
        text: 注释的文本内容。
        timeStart: 注释显示的开始时间，为 datetime 对象。
        timeEnd: 注释显示的结束时间，为 datetime 对象。
        x: 注释左上角的 x 坐标 (视频宽度的百分比)。
        y: 注释左上角的 y 坐标 (视频高度的百分比)。
        width: 注释的宽度 (视频宽度的百分比)。
        height: 注释的高度 (视频高度的百分比)。
        sx: 气泡注释箭头/锚点的 x 坐标 (视频宽度的百分比)。
            适用于气泡样式的注释。
        sy: 气泡注释箭头/锚点的 y 坐标 (视频高度的百分比)。
            适用于气泡样式的注释。
        bgOpacity: 注释的背景不透明度，为 `Alpha` 对象。
        bgColor: 注释的背景颜色，为 `Color` 对象。
        fgColor: 注释的前景 (文本) 颜色，为 `Color` 对象。
        textSize: 字体大小，通常是相对于视频高度的百分比。
        fontWeight: 字体粗细 (例如 "bold")。
        ref: 用于触发机制的引用注释的标识符。
    """

    # 致谢 https://github.com/isaackd/annotationlib
    # 这是 annotationlib "简易结构" 的一个模仿
    # 将 Annotation 抽成简单的结构让事情变得简单起来

    # 随着 Google 关闭 Annotations,
    # Annotations 已成黑盒
    # 你应当了解
    # 本项目对 Annotations 的猜测并不准确
    # 更何况我没有写过 CSS :-)

    def __init__(self):
        self.id: str = ""
        # 这里仅列出需要的 type 和 style, 且 Literal 仅做提醒作用
        self.type: Union[
            Literal[
                "text",
                "highlight",
                # branding
                # card
                # drawer
                # promotion
                # pause
            ],
            str,
        ] = "text"
        self.style: Union[
            Literal[
                "popup",
                "title",
                "speech",
                "highlightText",
                "anchored",
                "label",
                "",
                # branding
                # channel
                # cta
                # playlist
                # subscribe
                # video
                # vote
                # website
                # simple
                # poll
                # collaboration
                # donation
                # movie
                # episode
            ],
            str,
        ] = "popup"
        self.author: str = ""
        self.text: str = ""
        # fmt: off
        self.timeStart: datetime = datetime.strptime("0", "%S")
        self.timeEnd:   datetime = datetime.strptime("0", "%S")
        # fmt: on

        # Annotations 的定位全部是 "百分比", SSA 能正确显示真是谢天谢地
        self.x: float = 0.0
        self.y: float = 0.0
        # width(w), height(h) 是文本框的宽高
        self.width: float = 0.0
        self.height: float = 0.0
        # sx, sy 是 speech 样式的气泡锚点
        self.sx: float = 0.0
        self.sy: float = 0.0
        # bgOpacity(bgAlpha) 是注释文本后面那个框的不透明度
        # Annotations 用一个小数表示不透明度
        self.bgOpacity: Alpha = Alpha(alpha=204)
        # bgColor 是注释文本后面那个框的颜色
        self.bgColor: Color = Color(red=255, green=255, blue=255)
        # fgColor 是注释文本的颜色
        # 如果不是 Annotations, 我都不知道颜色值可以用十进制表达, 而且还是BGR, 视频出来效果不对才知道
        self.fgColor: Color = Color(red=0, green=0, blue=0)
        # textSize 是 "文字占画布的百分比"
        self.textSize: float = 3.15
        # fontWeight 是字重
        self.fontWeight: str = ""
        # 一些注释会在触发后才显示
        self.ref: str = ""
        # SSA 不能实现交互,
        # 处理 action 没有意义
        # self.actionType: Literal["time", "url"] = "time"
        # self.target: str = ""
        # self.url: str = ""
        # self.actionSeconds: datetime = datetime.strptime("0", "%S")
        # self.highlightId: str = ""

    def __str__(self) -> str:
        # 模仿 https://github.com/isaackd/annotations-converter

        def f(color: Color) -> int:
            return (color.blue << 16) | (color.green << 8) | color.red

        bgc = f(self.bgColor)
        bgo = self.bgOpacity.alpha / 255
        fgc = f(self.bgColor)
        ts = datetime.strftime(self.timeStart, "%S")
        te = datetime.strftime(self.timeStart, "%S")
        return f"bgc={bgc},bgo={bgo},fgc={fgc},txsz={self.textSize},tp={self.type},x={self.x},y={self.y},w={self.width},h={self.height},ts={ts},te={te},s={self.style},t={self.text}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, value: object) -> bool:
        return str(self) == str(value)


def Parse(tree: Element) -> List[Annotation]:
    """解析 XML 元素树并提取 YouTube 注释数据。

    此函数导航 XML 结构（通常从 YouTube `annotations.xml` 文件解析而来），
    以查找和解释单个注释元素。它为每个注释提取各种属性，如时间、文本、
    位置和样式，并填充 `Annotation` 对象列表。
    内部辅助函数用于从 XML 中的字符串表示形式解析特定数据类型，
    如颜色、时间值和浮点数。

    参数:
        tree: 已解析注释 XML 文档的根 `xml.etree.ElementTree.Element`。

    返回:
        `Annotation` 对象列表，每个对象代表从输入 XML 解析的注释。
        如果未找到有效注释，则返回空列表。

    引发:
        NotAnnotationsDocumentError: 如果提供的 XML 树不符合预期的 YouTube
                                     注释结构（例如，缺少 'annotations' 元素）。
    """

    # 本质上在提取和清理数据

    # Annotation 文件是一个 XML 文件
    # 详细结构可以看看 src/tests/testCase/Baseline/*.xml.test

    def ParseAnnotationAlpha(alphaString: str) -> Alpha:
        """
        解析 Annotation 的透明度
        "0.600000023842" -> Alpha(alpha=102)
        """
        alpha = int(float(alphaString) * 255) & 255
        return Alpha(alpha=alpha)

    def ParseAnnotationColor(colorString: str) -> Color:
        """
        解析 Annotation 的颜色值
        "4210330" -> Color(red=154, green=62, blue=64)
        """
        integer = int(colorString)
        r = integer & 255
        g = (integer >> 8) & 255
        b = integer >> 16 & 255
        return Color(red=r, green=g, blue=b)

    def ParseTime(timeString: str) -> datetime:
        def parseFloat(string: str) -> float:
            def cleanInt(string: str) -> str:
                string = string.replace("s", "")
                string = string.replace("-", "")
                string = string.replace("%", "")

                if string == "NaN":
                    return "0"
                if string == "aN":
                    return "0"
                if "#" in string:
                    return "0"
                return string

            if string == "":
                return 0
            if string == "4294967294":
                return 0
            if string == "&":
                return 0
            if string == "NaN":
                return 0

            part = string.split(".")
            part = list(map(cleanInt, part))
            string = part[0]
            if len(part) > 1:
                string = string + "." + part[1]
            return float(string)

        if timeString == "":
            return datetime.strptime("0", "%S")
        if timeString == "never":
            return datetime.strptime("0", "%S")
        if timeString == "undefined":
            return datetime.strptime("0", "%S")

        parts = timeString.split(":")
        seconds = 0.0

        for part in parts:
            time = parseFloat(part)
            seconds = 60 * seconds + abs(time)

        return datetime.fromtimestamp(seconds, dt.timezone.utc).replace(tzinfo=None)

    def ParseFloat(string: str) -> float:
        string = string.replace(",", ".")
        return float(string)

    def ParseAnnotation(each: Element) -> Optional[Annotation]:
        # 致谢: https://github.com/nirbheek/youtube-ass
        #    & https://github.com/isaackd/annotationlib

        _id = each.get("id", "")
        if _id == "":
            return None

        _type = each.get("type", "")
        if _type == "":
            return None
        if _type not in ("text", "highlight"):
            Stderr(_('不支持 "{}" 类型 ({})').format(_type, _id))
            return None

        style = each.get("style", "")

        if style == "" and _type != "highlight":
            Info(_('"{}" 没有 style, 跳过').format(_id))
            return None

        text = ""
        text_element = each.find("TEXT")
        if text_element is not None:
            if isinstance(text_element.text, str):
                text = text_element.text

        _Segment = each.find("segment")
        if _Segment is None:
            Info(_('"{}" 没有 segment, 跳过').format(_id))
            return None

        MovingRegion = _Segment.find("movingRegion")
        if MovingRegion is None:
            Info(_('"{}" 没有 movingRegion, 跳过').format(_id))
            return None

        Segment = MovingRegion.findall("rectRegion")
        if len(Segment) == 0:
            Segment = MovingRegion.findall("anchoredRegion")
        if len(Segment) == 0:
            Segment = MovingRegion.findall("shapelessRegion")
        if len(Segment) == 0 and style != "highlightText":
            Info(_('"{}" 没有时间, 跳过').format(_id))
            return None

        t1 = t2 = ""
        t1 = Segment[0].get("t", "")
        if len(Segment) >= 2:
            t2 = Segment[1].get("t", "")

        Start = ParseTime(min(t1, t2))
        End = ParseTime(max(t1, t2))

        # 两个 Segment 只有时间差别
        x = ParseFloat(Segment[0].get("x", "0"))
        y = ParseFloat(Segment[0].get("y", "0"))
        w = ParseFloat(Segment[0].get("w", "0"))
        h = ParseFloat(Segment[0].get("h", "0"))
        sx = ParseFloat(Segment[0].get("sx", "0"))
        sy = ParseFloat(Segment[0].get("sy", "0"))

        author = each.get("author", "")

        if w < 0:
            w = 0
        if math.isnan(w):
            w = 0

        annotation = Annotation()

        annotation.id = _id
        annotation.type = _type
        annotation.style = style
        annotation.text = text
        annotation.timeStart = Start
        annotation.timeEnd = End
        annotation.x = x
        annotation.y = y
        annotation.width = w
        annotation.height = h
        annotation.sx = sx
        annotation.sy = sy
        annotation.author = author

        Appearance = each.find("appearance")

        if Appearance is not None:
            bgAlpha = Appearance.get("bgAlpha", "0.8")
            bgColor = Appearance.get("bgColor", "16777215")
            fgColor = Appearance.get("fgColor", "0")
            textSize = Appearance.get("textSize", "3.15")
            fontWeight = Appearance.get("fontWeight", "")

            annotation.bgOpacity = ParseAnnotationAlpha(bgAlpha)
            annotation.bgColor = ParseAnnotationColor(bgColor)
            annotation.fgColor = ParseAnnotationColor(fgColor)
            annotation.textSize = ParseFloat(textSize)
            annotation.fontWeight = fontWeight

        ref = ""
        Trigger = each.find("trigger")
        if Trigger is not None:
            Condition = Trigger.find("condition")
            if Condition is not None:
                ref = Condition.get("ref", "")

        annotation.ref = ref

        return annotation

    annotations_tree = tree.find("annotations")
    if annotations_tree is None:
        raise NotAnnotationsDocumentError(_("不是 Annotations 文档"))

    annotations: List[Annotation] = []
    for each in annotations_tree.findall("annotation"):
        annotation = ParseAnnotation(each)
        if annotation is not None:
            annotations.append(annotation)

    return annotations
