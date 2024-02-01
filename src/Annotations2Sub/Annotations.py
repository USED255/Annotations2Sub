#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Annotations 相关"""

from datetime import datetime
from typing import List, Optional, Union
from xml.etree.ElementTree import Element

from Annotations2Sub.Color import Alpha, Color
from Annotations2Sub.utils import Info, Stderr, _

# 兼容 Python3.6, 3.7
# Python3.6, 3.7 的 typing 没有 Literal
try:
    from typing import Literal
except ImportError:
    pass


def Dummy(*args, **kwargs):
    """用于 MonkeyPatch"""


class Annotation:
    """Annotation 结构"""

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
        self.type: Union[Literal["text", "highlight", "branding"], str] = "text"
        # 现在就遇到这几个样式
        self.style: Union[
            Literal[
                "popup",
                "title",
                "speech",
                "highlightText",
                "anchored",
                # branding
                # channel
                # cta
                # label
                # playlist
                # subscribe
                # video
                # vote
                # website
            ],
            str,
        ] = "popup"
        self.text: str = ""
        self.timeStart: datetime = datetime.strptime("0", "%S")
        self.timeEnd: datetime = datetime.strptime("0", "%S")
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
        # textSize 是 "文字占画布的百分比", 而在 title 样式中才是熟悉的 "字体大小"
        self.textSize: float = 3.15
        self.author: str = ""
        self.fontWeight: str = ""
        self.effects: str = ""
        # SSA 不能实现交互,
        # 处理 action 没有意义
        # self.actionType: Literal["time", "url"] = "time"
        # self.actionUrl: str = ""
        # self.actionUrlTarget: str = ""
        # self.actionSeconds: datetime = datetime.strptime("0", "%S")
        # self.highlightId: str = ""


def Parse(tree: Element) -> List[Annotation]:
    """将 XML 树转换为 List[Annotation]"""

    # Annotation 文件是一个 XML 文件
    # 详细结构可以看看 src/tests/testCase/annotation.xml.test

    def ParseAnnotationAlpha(alpha: str) -> Alpha:
        """
        解析 Annotation 的透明度
        "0.600000023842" -> Alpha(alpha=102)
        """
        if alpha == None:
            raise ValueError(_('"alpha" 不应为 None'))
        variable1 = float(alpha) * 255
        return Alpha(alpha=int(variable1))

    def ParseAnnotationColor(color: str) -> Color:
        """
        解析 Annotation 的颜色值
        "4210330" -> Color(red=154, green=62, blue=64)
        """
        if color == None:
            raise ValueError(_('"color" 不应为 None'))
        integer = int(color)
        r = integer & 255
        g = (integer >> 8) & 255
        b = integer >> 16
        return Color(red=r, green=g, blue=b)

    def ParseTime(timeString: str) -> datetime:
        colon_count = timeString.count(":")
        time_format = ""
        if colon_count == 2:
            time_format += "%H:"
        time_format += "%M:%S"
        if "." in timeString:
            time_format += ".%f"
        time = datetime.strptime(timeString, time_format)
        return time

    def ParseAnnotation(each: Element) -> Optional[Annotation]:
        """解析 Annotation"""

        # 致谢: https://github.com/nirbheek/youtube-ass
        #    & https://github.com/isaackd/annotationlib

        _id = each.get("id", "")

        _type = each.get("type", "")
        if _type == "":
            return None
        if _type not in ("text", "highlight", "branding"):
            Stderr(_("不支持 {} 类型 ({})").format(_type, _id))
            return None

        style = each.get("style", "")

        if style == "" and _type != "highlight":
            Info(_("{} 没有 style, 跳过").format(_id))
            return None

        text = ""
        text_element = each.find("TEXT")
        if isinstance(text_element, Element):
            if isinstance(text_element.text, str):
                text = text_element.text

        _Segment = each.find("segment")
        if _Segment is None:
            Info(_("{} 没有 segment, 跳过").format(_id))
            return None

        _Segment = _Segment.find("movingRegion")
        if _Segment is None:
            Info(_("{} 没有 movingRegion, 跳过").format(_id))
            return None

        Segment = _Segment.findall("rectRegion")
        if len(Segment) == 0:
            Segment = _Segment.findall("anchoredRegion")
        if len(Segment) == 0:
            if style != "highlightText":
                Info(_("{} 没有时间, 跳过").format(_id))
                return None

        _Start = _End = "0:00:00.00"
        if style == "highlightText":
            _Start = "0:00:00.00"
            _End = "9:00:00.00"

        t1 = Segment[0].get("t", _Start)
        t2 = Segment[1].get("t", _End)
        if "never" in (t1, t2):
            Info(_("{} 不显示, 跳过").format(_id))
            return None

        Start = ParseTime(min(t1, t2))
        End = ParseTime(max(t1, t2))

        x = float(Segment[0].get("x", "0"))
        y = float(Segment[0].get("y", "0"))

        annotation = Annotation()

        annotation.id = _id
        annotation.type = _type
        annotation.style = style
        annotation.text = text
        annotation.timeStart = Start
        annotation.timeEnd = End
        annotation.x = x
        annotation.y = y

        # 两个 Segment 只有时间差别
        w = Segment[0].get("w", "0")
        h = Segment[0].get("h", "0")
        sx = Segment[0].get("sx", "0")
        sy = Segment[0].get("sy", "0")

        annotation.width = float(w)
        annotation.height = float(h)
        annotation.sx = float(sx)
        annotation.sy = float(sy)

        Appearance = each.find("appearance")

        # 如果没有 Appearance 下面这些都是有默认值的
        if Appearance is not None:
            bgAlpha = Appearance.get("bgAlpha", "0.8")
            bgColor = Appearance.get("bgColor", "16777215")
            fgColor = Appearance.get("fgColor", "0")
            textSize = Appearance.get("textSize", "3.15")
            fontWeight = Appearance.get("fontWeight", "")
            effects = Appearance.get("effects", "")

            annotation.bgOpacity = ParseAnnotationAlpha(bgAlpha)
            annotation.bgColor = ParseAnnotationColor(bgColor)
            annotation.fgColor = ParseAnnotationColor(fgColor)
            annotation.textSize = float(textSize)
            annotation.fontWeight = fontWeight
            annotation.effects = effects

        author = each.get("author", "")
        annotation.author = author

        return annotation

    Dummy([ParseAnnotationAlpha, ParseAnnotationColor])

    annotations_tree = tree.find("annotations")
    if annotations_tree is None:
        raise ValueError(_("不是 Annotations 文档"))

    annotations: List[Annotation] = []
    for each in annotations_tree.findall("annotation"):
        annotation = ParseAnnotation(each)
        if annotation is not None:
            annotations.append(annotation)

    return annotations
