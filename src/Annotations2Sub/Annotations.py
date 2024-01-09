#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Annotations 相关"""

import datetime
from typing import Any, List, Optional, Union


from xml.etree.ElementTree import Element

from Annotations2Sub.Color import Alpha, Color
from Annotations2Sub.utils import Flags, MakeSureStr, Stderr, _

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
    # 这是 annotationlib "简易结构" 的一个模仿, 命名遵循了其风格
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
        # 现在就遇到这几个样式, 不知道还有什么样式
        self.style: Union[
            Literal[
                "popup",
                "title",
                "speech",
                "highlightText",
                "anchored",
            ],
            str,
        ] = "popup"
        self.text: str = ""
        self.timeStart: datetime.datetime = datetime.datetime.strptime("0", "%S")
        self.timeEnd: datetime.datetime = datetime.datetime.strptime("0", "%S")
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
        # fgColor 就是注释文本的颜色
        # 如果不是 Annotations, 我都不知道颜色值可以用十进制表达, 而且还是BGR ,视频出来效果不对才知道
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
        # self.actionSeconds: datetime.datetime = datetime.datetime.strptime("0", "%S")
        # self.highlightId: str = ""


def Parse(tree: Element) -> List[Annotation]:
    """将 XML 树转换为 List[Annotation]"""

    # Annotation 文件是一个 XML 文件
    # 详细结构可以看看 src/tests/testCase/annotation.xml.test

    def ParseAnnotationAlpha(alpha: str) -> Alpha:
        """
        解析 Annotation 的透明度
        bgAlpha("0.600000023842") -> Alpha(alpha=102)
        """
        if alpha == None:
            raise ValueError(_('"alpha" 不应为 None'))
        variable1 = float(alpha) * 255
        return Alpha(alpha=int(variable1))

    def ParseAnnotationColor(color: str) -> Color:
        """
        解析 Annotation 的颜色值
        bgColor("4210330") -> Color(red=154, green=62, blue=64)
        """
        if color == None:
            raise ValueError(_('"color" 不应为 None'))
        integer = int(color)
        r = integer & 255
        g = (integer >> 8) & 255
        b = integer >> 16
        return Color(red=r, green=g, blue=b)

    def ParseTime(timeString: str) -> datetime.datetime:
        colon_count = timeString.count(":")
        time_format = ""
        if colon_count == 2:
            time_format += "%H:"
        time_format += "%M:%S"
        if "." in timeString:
            time_format += ".%f"
        time = datetime.datetime.strptime(timeString, time_format)
        return time

    def MakeSureElement(element: Any) -> Element:
        """确保是 Element"""
        if isinstance(element, Element):
            return element
        raise TypeError(_("不是 Element 类型"))

    def ParseAnnotation(each: Element) -> Optional[Annotation]:
        """解析 Annotation"""

        # 致谢: https://github.com/nirbheek/youtube-ass
        #    & https://github.com/isaackd/annotationlib

        _id = MakeSureStr(each.get("id"))

        # 依照
        # https://github.com/isaackd/annotationlib/blob/0818bddadade8dd1d13f3006e34a5837a539567f/src/parser/index.js#L129
        # 所说
        # 这里可能有 text, highlight, pause, branding 类型
        # branding 我不知道是啥
        # pause 应该不能实现,
        # 我相信字幕滤镜不会闲的蛋疼实现暂停功能
        # 而且 annotationlib 也不处理 pause
        # annotationlib 也不处理空的 type
        __type = each.get("type")
        if __type == None:
            return None
        _type = MakeSureStr(__type)
        del __type
        if _type not in ("text", "highlight", "branding"):
            Stderr(_("不支持 {} 类型 ({})").format(_type, _id))
            # 我不知道显式的 return None 有什么用
            # 但是 annotationlib 是这样做的
            # 我也学学
            return None

        style = each.get("style")
        if style == None and _type == "highlight":
            style = ""
        if style == None:
            if Flags.verbose:
                Stderr(_("{} 没有 style, 跳过").format(_id))
            return None
        style = MakeSureStr(style)

        text = ""
        __text = each.find("TEXT")
        # 根据经验, 空的 TEXT 只是没有文本, 不是没有内容
        if __text == None:
            text = ""
        if isinstance(__text, Element):
            _text = __text.text
            del __text
            text = MakeSureStr(_text)
            del _text

        _Segment = each.find("segment")
        if _Segment is None:
            if Flags.verbose:
                Stderr(_("{} 没有 segment, 跳过").format(_id))
            return None
        _Segment = _Segment.find("movingRegion")
        if _Segment == None:
            # 学习 annotationlib
            # https://github.com/isaackd/annotationlib/blob/0818bddadade8dd1d13f3006e34a5837a539567f/src/parser/index.js#L117
            # 跳过没有内容的 Annotation
            # 之前(f20f9fe fixbugs)学的是 youtube-ass(https://github.com/nirbheek/youtube-ass)
            # 只是简单地把时间置零
            if Flags.verbose:
                Stderr(_("{} 没有 movingRegion, 跳过").format(_id))
            return None

        _Segment = MakeSureElement(_Segment)
        Segment = _Segment.findall("rectRegion")
        if len(Segment) == 0:
            # 在这之前(bdb6559 更新), 这里莫名其妙的包了个括号
            # 我把整个代码注释一遍原因之一就是为了发现这些问题
            # 而且这些代码是经验堆积而成, 我希望丰富的注释可以帮助路人理解这些代码怎么运行
            Segment = _Segment.findall("anchoredRegion")

        if len(Segment) == 0:
            if style != "highlightText":
                # 抄自 https://github.com/isaackd/annotationlib/blob/0818bddadade8dd1d13f3006e34a5837a539567f/src/parser/index.js#L121
                # 不过我现在没见过 highlightText
                # 我选择相信别人的经验
                # 我猜 highlightText 一直在屏幕上, 需要手动关闭
                if Flags.verbose:
                    Stderr(_("{} 没有时间, 跳过").format(_id))
                return None

        _Start = _End = "0:00:00.00"
        if style == "highlightText":
            _Start = "0:00:00.00"
            _End = "9:00:00.00"

        t1 = MakeSureStr(Segment[0].get("t"))
        t2 = MakeSureStr(Segment[1].get("t"))
        if "never" in (t1, t2):
            # 跳过不显示的 Annotation
            if Flags.verbose:
                Stderr(_("{} 不显示, 跳过").format(_id))
            return None

        _Start = min(t1, t2)
        _End = max(t1, t2)

        Start = ParseTime(_Start)
        End = ParseTime(_End)

        del _Start
        del _End

        x = float(MakeSureStr(Segment[0].get("x")))
        y = float(MakeSureStr(Segment[0].get("y")))

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
        w = Segment[0].get("w")
        h = Segment[0].get("h")
        sx = Segment[0].get("sx")
        sy = Segment[0].get("sy")

        # 在之前用的是 if x is not None:, 其他人有用 if x:
        # 我觉得 if x: 用在布尔值上比较好
        # is not 就算了
        # 所以用了 if x != None:
        if w != None:
            annotation.width = float(MakeSureStr(w))
        if h != None:
            annotation.height = float(MakeSureStr(h))
        if sx != None:
            annotation.sx = float(MakeSureStr(sx))
        if sy != None:
            annotation.sy = float(MakeSureStr(sy))

        Appearance = each.find("appearance")

        # 如果没有 Appearance 下面这些都是有默认值的
        if Appearance != None:
            Appearance = MakeSureElement(Appearance)
            bgAlpha = Appearance.get("bgAlpha")
            bgColor = Appearance.get("bgColor")
            fgColor = Appearance.get("fgColor")
            textSize = Appearance.get("textSize")
            fontWeight = Appearance.get("fontWeight")
            effects = Appearance.get("effects")

            if bgAlpha != None:
                annotation.bgOpacity = ParseAnnotationAlpha(MakeSureStr(bgAlpha))
            if bgColor != None:
                annotation.bgColor = ParseAnnotationColor(MakeSureStr(bgColor))
            if fgColor != None:
                annotation.fgColor = ParseAnnotationColor(MakeSureStr(fgColor))
            if textSize != None:
                annotation.textSize = float(MakeSureStr(textSize))
            if fontWeight != None:
                annotation.fontWeight = MakeSureStr(fontWeight)
            if effects != None:
                annotation.effects = MakeSureStr(effects)

        author = each.get("author")
        if author != None:
            author = MakeSureStr(author)
            annotation.author = author

        return annotation

    Dummy([ParseAnnotationAlpha, ParseAnnotationColor, MakeSureElement])

    try:
        annotations_tree = MakeSureElement(tree.find("annotations"))
    except TypeError:
        raise ValueError(_("不是 Annotations 文档"))

    annotations: List[Annotation] = []
    for each in annotations_tree.findall("annotation"):
        annotation = ParseAnnotation(each)
        if isinstance(annotation, Annotation):
            annotations.append(annotation)

    return annotations
