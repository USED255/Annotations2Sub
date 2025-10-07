# -*- coding: utf-8 -*-

import datetime as dt
import math
from datetime import datetime
from typing import List, Optional, Union
from xml.etree.ElementTree import Element

from Annotations2Sub.color import Alpha, Color
from Annotations2Sub.i18n import _
from Annotations2Sub.utils import Info, Stderr

# 兼容 Python 3.7
# Python 3.7 的 typing 没有 Literal
try:
    from typing import Literal
except ImportError:
    pass


class NotAnnotationsDocumentError(ValueError):
    pass


class Annotation:
    """Annotation 结构"""

    # 致谢 https://github.com/isaackd/annotationlib
    # 这是 annotationlib "简易结构" 的一个模仿
    # 将 Annotation 抽成简单的结构让事情变得简单起来

    # 如果您需要详细了解 Annotation, 请参阅 https://github.com/USED255/youtube_annotations_hack

    def __init__(self):
        self.id: str = ""
        # 这里仅列出需要的 type 和 style
        self.type: Union[
            Literal[
                "text",
                "highlight",
                # 字幕滤镜无法实现暂停
                # "pause",
                #
                # 以下是 Youtube Card 和 End screens 的类型,
                # Youtube Card 可以看做现代化的 Annotations,
                # 与 Annotations 共用代码库, 所以会出现在 Annotations 文件中.
                # 但是 Card 不是 Annotations, 处理其没有意义.
                # "branding",
                # "card",
                # "drawer",
                # "promotion",
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
                # "highlight" 类型没有 style
                "",
                # "branding",
                # "channel",
                # "cta",
                # "playlist",
                # "subscribe",
                # "video",
                # "vote",
                # "website",
                # "simple",
                # "poll",
                # "collaboration",
                # "donation",
                # "movie",
                # "episode",
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
        # 我没有观察到 effects 的效果, 暂不实现.
        # self.effects: str = ""
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
        # 方便调试
        return str(self)

    def __eq__(self, value: object) -> bool:
        # 没有用到这个功能
        return str(self) == str(value)


def Parse(tree: Element) -> List[Annotation]:
    """解析 Annotations 树"""

    # 本质上在提取和清理数据

    # Annotation 文件是一个 XML 文件
    # 详细结构可以看看 src/tests/testCase/Baseline/*.xml.test

    def ParseAnnotation(each: Element) -> Optional[Annotation]:
        # 致谢: https://github.com/nirbheek/youtube-ass
        #    & https://github.com/isaackd/annotationlib

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

        _id = each.get("id", "")
        if _id == "":
            Info(_('"{}" 没有 id, 跳过').format(_id))
            return None

        _type = each.get("type", "")
        if _type == "":
            Info(_('"{}" 没有 type, 跳过').format(_id))
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
        if text_element != None:
            if text_element.text != None:
                text = text_element.text

        _Segment = each.find("segment")
        if _Segment == None:
            Info(_('"{}" 没有 segment, 跳过').format(_id))
            return None

        MovingRegion = _Segment.find("movingRegion")
        if MovingRegion == None:
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

        if w < 0:
            w = 0
        if math.isnan(w):
            w = 0

        author = each.get("author", "")

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

        if Appearance != None:
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

        Trigger = each.find("trigger")
        if Trigger != None:
            Condition = Trigger.find("condition")
            if Condition != None:
                ref = Condition.get("ref", "")
                annotation.ref = ref

        return annotation

    annotations_tree = tree.find("annotations")
    if annotations_tree == None:
        raise NotAnnotationsDocumentError(_("不是 Annotations 文档"))

    annotations: List[Annotation] = []
    for each in annotations_tree.findall("annotation"):
        annotation = ParseAnnotation(each)
        if annotation != None:
            annotations.append(annotation)

    return annotations
