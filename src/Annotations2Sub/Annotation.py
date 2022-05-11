#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from typing import List, Optional
from xml.etree.ElementTree import Element

from Annotations2Sub.Color import Alpha, Color
from Annotations2Sub.internationalization import _

# 兼容 Python3.6
# Python3.6 的 typing 没有 Literal
try:
    from typing import Literal  # type: ignore
except:
    pass


class Annotation(object):
    # 致谢 https://github.com/isaackd/annotationlib
    # 这其实是 annotationlib "简易结构" 的一个移植
    # 命名遵循了其实现, 并没有按我的喜好更改
    # 将 Annotation 抽成了简单的结构确实让事情变得简单了很多
    """Annotation 结构"""

    # 随着 Google 关闭 Annotation,
    # Annotation 已成黑盒
    # 你应当了解
    # 本项目对 Annotation 的揣测并不准确
    # 更何况我并没有写过 CSS :-)

    def __init__(self):
        # 这里仅列出了需要的结构
        # 如 highlightId action 等没有列出
        # SSA(Sub Station Alpha) 并不能实现交互, 所以处理 action 没有意义
        self.id: str = ""
        # 这里仅列出需要的 type 和 style, 且 Literal 仅做提醒作用
        self.type: Literal["text", "highlight", "branding"] = ""
        # 我现在就遇到这四个样式, 不知道还有什么样式
        self.style: Literal[
            "popup",
            "title",
            "speech",
            "highlightText",
        ] = ""
        self.text: str = ""
        # 一个结构化的时间显然比字符串好
        self.timeStart: datetime.datetime = datetime.datetime.strptime("0", "%S")
        self.timeEnd: datetime.datetime = datetime.datetime.strptime("0", "%S")
        # Annotation 的定位全部是 "百分比", 还可能是用 CSS 实现的, SSA 能正确显示真是谢天谢地
        self.x: float = 0.0
        self.y: float = 0.0
        # width, height 是文本框的宽高
        # 按我的喜好我想将其写为 w, h
        self.width: float = 0.0
        self.height: float = 0.0
        # sx, sy 是 speech 样式的气泡锚点
        self.sx: float = 0.0
        self.sy: float = 0.0
        # Annotation 用一个小数表示透明度, 不过我其实到现在都不知道哪个是透明哪个是不透明, 等我拿到测试用例着吧
        # 按我的喜好我想将其写为 bgAlpha
        self.bgOpacity: Alpha = Alpha(alpha=204)
        # 如果不是 Annotation, 我都不知道颜色值可以用十进制表达
        # 类似于 bgOpacity , 开始我也不知道这玩耶是 BGR ,是视频出来效果不对才知道
        # 一个结构化的颜色显然比奇怪的颜色值容易理解得多
        self.bgColor: Color = Color(red=255, green=255, blue=255)
        self.fgColor: Color = Color(red=0, green=0, blue=0)
        # 注意的是, textSize 是个"百分比",而在 title 样式中才是熟悉的 "字体大小"
        self.textSize: float = 3.15
        # 这里相比 annotationlib 少了
        #     actionType
        #     actionUrl
        #     actionUrlTarget
        #     actionSeconds


def Parse(tree: Element) -> List[Annotation]:
    """将 XML 树转换为 List[Annotation]"""

    def ParseAnnotationAlpha(s: str) -> Alpha:
        """
        解析 Annotation 的透明度
        bgAlpha="0.600000023842" -> Alpha(alpha=102)
        """
        if s is None:
            raise Exception("alpha is None")
        s1 = float(s)
        s2 = 1 - s1
        s3 = s2 * 255
        s4 = int(s3)
        return Alpha(alpha=s4)

    def ParseAnnotationColor(s: str) -> Color:
        """
        解析 Annotation 的颜色值
        bgColor="4210330" -> Color(red=154, green=62, blue=64)
        """
        if s is None:
            raise Exception("color is None")
        s1 = int(s)
        # 如何分离数字我早还给高中老师了, 这里是 GitHub Cockpit 帮我写的, 当然写出来是错的, 帮忙改了改
        r = s1 & 255
        g = (s1 >> 8) & 255
        b = s1 >> 16
        return Color(red=r, green=g, blue=b)

    def MakeSureStr(s: Optional[str]) -> str:
        # 这个是用来应付类型注释了, 我觉得在输入确定的环境里做类型检查没有必要
        if isinstance(s, str):
            return str(s)
        raise TypeError

    def ParseAnnotation(each: Element) -> Optional[Annotation]:
        # 致谢: https://github.com/nirbheek/youtube-ass
        # 致谢: https://github.com/isaackd/annotationlib
        annotation = Annotation()

        annotation.id = MakeSureStr(each.get("id"))

        type = each.get("type")
        # 依照
        # https://github.com/isaackd/annotationlib/blob/0818bddadade8dd1d13f3006e34a5837a539567f/src/parser/index.js#L129
        # 所说
        # 这里可能有 text, highlight, pause, branding 类型
        # branding 我不知道是啥
        # pause 应该不能实现,
        # 我相信字幕滤镜不会闲的蛋疼实现暂停功能
        if type not in ("text", "highlight", "branding"):
            print(_("不支持{}类型. ()").format(type, annotation.id))
            return None
        annotation.type = MakeSureStr(type)  # type: ignore

        style = each.get("style")
        #
        if style is None:
            return None
        annotation.style = style  # type: ignore

        text = each.find("TEXT")
        if text is None:
            annotation.text = ""
        else:
            annotation.text = MakeSureStr(text.text)

        if len(each.find("segment").find("movingRegion")) == 0:  # type: ignore
            # 跳过没有内容的 Annotation
            return None

        Segment = each.find("segment").find("movingRegion").findall("rectRegion")  # type: ignore
        if len(Segment) == 0:
            Segment = (
                each.find("segment").find("movingRegion").findall("anchoredRegion")  # type: ignore
            )

        if len(Segment) == 0:
            if annotation.style != "highlightText":
                # 抄自 https://github.com/isaackd/annotationlib/blob/0818bddadade8dd1d13f3006e34a5837a539567f/src/parser/index.js#L121
                return None

        if len(Segment) != 0:
            t1 = MakeSureStr(Segment[0].get("t"))
            t2 = MakeSureStr(Segment[1].get("t"))
            Start = min(t1, t2)
            End = max(t1, t2)

        if "never" in (Start, End):
            # 跳过不显示的 Annotation
            return None

        try:
            annotation.timeStart = datetime.datetime.strptime(Start, "%H:%M:%S.%f")
            annotation.timeEnd = datetime.datetime.strptime(End, "%H:%M:%S.%f")
        except:
            annotation.timeStart = datetime.datetime.strptime(Start, "%M:%S.%f")
            annotation.timeEnd = datetime.datetime.strptime(End, "%M:%S.%f")

        annotation.x = float(MakeSureStr(Segment[0].get("x")))
        annotation.y = float(MakeSureStr(Segment[0].get("y")))

        w = Segment[0].get("w")
        h = Segment[0].get("h")
        sx = Segment[0].get("sx")
        sy = Segment[0].get("sy")

        if w != None:
            annotation.width = float(MakeSureStr(w))
        if h != None:
            annotation.height = float(MakeSureStr(h))
        if sx != None:
            annotation.sx = float(MakeSureStr(sx))
        if sy != None:
            annotation.sy = float(MakeSureStr(sy))

        Appearance = each.find("appearance")

        if Appearance != None:
            bgAlpha = Appearance.get("bgAlpha")  # type: ignore
            bgColor = Appearance.get("bgColor")  # type: ignore
            fgColor = Appearance.get("fgColor")  # type: ignore
            textSize = Appearance.get("textSize")  # type: ignore

            if bgAlpha != None:
                annotation.bgOpacity = ParseAnnotationAlpha(MakeSureStr(bgAlpha))
            if bgColor != None:
                annotation.bgColor = ParseAnnotationColor(MakeSureStr(bgColor))
            if fgColor != None:
                annotation.fgColor = ParseAnnotationColor(MakeSureStr(fgColor))
            if textSize != None:
                annotation.textSize = float(MakeSureStr(textSize))

        return annotation

    annotations: List[Annotation] = []
    for each in tree.find("annotations").findall("annotation"):  # type: ignore
        annotation = ParseAnnotation(each)
        if annotation != None:
            annotations.append(annotation)  # type: ignore

    return annotations
