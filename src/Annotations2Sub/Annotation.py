#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from typing import List, Optional
from xml.etree.ElementTree import Element
from Annotations2Sub.flag import Flags

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
    # 在在此之前(f20f9f fixbugs) XML 树就直接转换为 Event 了
    # 代码随着时间推移变得很糟
    # 幸好当初没傻到直接吐出来字符串

    # 在这之前我还想过从树到 Event 是一个完美的管线
    # 然后遇到了 None 和 多个 Event
    # 还是吐出来一个 List 比较好

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

        _type = each.get("type")
        # 依照
        # https://github.com/isaackd/annotationlib/blob/0818bddadade8dd1d13f3006e34a5837a539567f/src/parser/index.js#L129
        # 所说
        # 这里可能有 text, highlight, pause, branding 类型
        # branding 我不知道是啥
        # pause 应该不能实现,
        # 我相信字幕滤镜不会闲的蛋疼实现暂停功能
        # 而且 annotationlib 也不处理 pause
        # annotationlib 也不处理空的 type
        # 但是我还没有遇到过
        if _type not in ("text", "highlight", "branding"):
            print(_("不支持{}类型 ({})").format(_type, annotation.id))
            # 我不知道显式的 return None 有什么用
            # 但是 annotationlib 是这样做的
            # 我也学学
            return None
        # 类型检查可以避免些低级错误, 提升体验, 虽然在 Python 上有些瓦店房化
        annotation.type = MakeSureStr(_type)  # type: ignore

        style = each.get("style")
        # 根据经验, ,没有 style 也就没有内容
        if style is None:
            if Flags.verbose:
                print(_("{} 没有 style, 跳过").format(annotation.id))
            return None
        annotation.style = style  # type: ignore

        text = each.find("TEXT")
        # 根据经验, 空的 TEXT 只是没有文本, 不是没有内容
        if text is None:
            annotation.text = ""
        else:
            annotation.text = MakeSureStr(text.text)

        if len(each.find("segment").find("movingRegion")) == 0:  # type: ignore
            # 学习 annotationlib
            # https://github.com/isaackd/annotationlib/blob/0818bddadade8dd1d13f3006e34a5837a539567f/src/parser/index.js#L117
            # 跳过没有内容的 Annotation
            # 之前(f20f9f fixbugs)学的是 youtube-ass(https://github.com/nirbheek/youtube-ass)
            # 只是简单地把时间置零
            if Flags.verbose:
                print(_("{} 没有 movingRegion, 跳过").format(annotation.id))
            return None

        Segment = each.find("segment").find("movingRegion").findall("rectRegion")  # type: ignore
        if len(Segment) == 0:
            # 在这之前(bdb655 更新), 这里有个莫名其妙的包了个括号
            # 我把整个代码注释一遍原因之一就是为了发现这些问题
            # 而且这些代码其实是经验堆积成的, 我希望丰富的注释可以帮助路人理解这些代码是怎么来的
            Segment = each.find("segment").find("movingRegion").findall("anchoredRegion")  # type: ignore

        if len(Segment) == 0:
            if annotation.style != "highlightText":
                # 抄自 https://github.com/isaackd/annotationlib/blob/0818bddadade8dd1d13f3006e34a5837a539567f/src/parser/index.js#L121
                # 不过我现在没见过 highlightText
                # 不理解为什么 highlightText 可以没有时间
                # 我选择相信别人的经验
                # 毕竟我也没咋看过 Youtube
                if Flags.verbose:
                    print(_("{} highlightText 没有时间, 跳过").format(annotation.id))
                return None

        if len(Segment) != 0:
            t1 = MakeSureStr(Segment[0].get("t"))
            t2 = MakeSureStr(Segment[1].get("t"))
            Start = min(t1, t2)
            End = max(t1, t2)

        if "never" in (Start, End):
            # 跳过不显示的 Annotation
            # 之前(f20f9f fixbugs)不会英语, 理解成了相反的意思
            # 哈哈
            if Flags.verbose:
                print(_("{} 不显示, 跳过").format(annotation.id))
            return None

        # 其实这些字符串可以直接在 SSA 上用的, 但是不知道为什么之前(f20f9f fixbugs)来回转换了两次
        # 那些代码已经是两年前写的了
        # 我也忘了
        try:
            annotation.timeStart = datetime.datetime.strptime(Start, "%H:%M:%S.%f")
            # 在这之前(f20f9f fixbugs)我会在这里 ↓ 加两个空格与上面对齐, 但是 black 好像不太喜欢
            annotation.timeEnd = datetime.datetime.strptime(End, "%H:%M:%S.%f")
        except:
            annotation.timeStart = datetime.datetime.strptime(Start, "%M:%S.%f")
            annotation.timeEnd = datetime.datetime.strptime(End, "%M:%S.%f")

        annotation.x = float(MakeSureStr(Segment[0].get("x")))
        annotation.y = float(MakeSureStr(Segment[0].get("y")))

        # 我猜应该没有多个 Segment
        w = Segment[0].get("w")
        h = Segment[0].get("h")
        sx = Segment[0].get("sx")
        sy = Segment[0].get("sy")

        # 在之前(f20f9f fixbugs) 用的是 if x is not None:, 其他人用的是 if x:
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
    # 下面这行代码先从 youtube-ass 传到之前的 Annotations2Sub, 再从之前的 Annotations2Sub 传到这里
    for each in tree.find("annotations").findall("annotation"):  # type: ignore
        annotation = ParseAnnotation(each)
        if annotation != None:
            # 我想这个类型检查真是奇怪, 但是我也不知道该怎么做
            annotations.append(annotation)  # type: ignore

    return annotations
