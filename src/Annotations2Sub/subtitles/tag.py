from Annotations2Sub.color import Alpha, Color
from Annotations2Sub.subtitles.utils import Literal, _round


class Tags(list):
    """样式复写代码, 样式复写标签, ASS 标签, 特效标签, Aegisub 特效标签, 标签"""

    def __str__(self) -> str:
        tag_string = ""
        for tag in self:
            tag_string += str(tag)
        tag_string = r"{" + tag_string + r"}"
        return tag_string


class Align:
    r"""\an<位置>"""

    # "<位置> 是一个数字，决定了字幕显示在屏幕上哪个位置。"
    # 默认 SSA 定位会定在"2"(底部居中)
    # 用 \an7 指定在左上角.
    # fmt: off
    def __init__(self, align: Literal[7,8,9,
                                        4,5,6,
                                        1,2,3] ):
    # fmt: on
        self.align = align

    def __str__(self) -> str:
        return rf"\an{self.align}"


class Pos:
    r"""\pos(<x>,<y>)"""

    # "将字幕定位在坐标点 <x>,<y>。"
    # SSA 和 Annotations 坐标系一致, y 向下(左手取向).
    def __init__(self, x: float, y: float):
        self.x = _round(x)
        self.y = _round(y)

    def __str__(self) -> str:
        return rf"\pos({self.x},{self.y})"


class Fontsize:
    r"""\fs<字体尺寸>"""

    # "<字体尺寸> 是一个数字，指定了字体的点的尺寸。"
    # "注意，这里的字体尺寸并不是字号的大小，\fs20 并不是字体大小（font-size）为 20px，"
    # "而是指其行高（line-height）为 20px，主要归咎于 VSFilter 使用的 Windows GDI 的字体接口。"
    # 不明白字体大小和行高有什么区别
    def __init__(self, size: float):
        self.size = _round(size)

    def __str__(self) -> str:
        return rf"\fs{self.size}"


class PrimaryColour:
    r"""\<颜色序号>c[&][H]<BBGGRR>[&]"""

    # "<BBGGRR> 是一个十六进制的 RGB 值，但颜色顺序相反，前导的 0 可以省略。"
    # "<颜色序号> 可选值为 1、2、3 和 4，分别对应单独设置 PrimaryColour、SecondaryColour、OutlineColor 和 BackColour"
    # "其中的 & 和 H 按规范应该是要有的，但是如果没有也能正常解析。"
    # PrimaryColour 填充颜色, SecondaryColour 卡拉OK变色, OutlineColor 边框颜色, BackColour 阴影颜色
    def __init__(self, colour: Color):
        self.colour = colour

    def __str__(self) -> str:
        def DumpColor(color: Color) -> str:
            return "&H{:02X}{:02X}{:02X}&".format(color.red, color.green, color.blue)

        return rf"\c{DumpColor(self.colour)}"


class PrimaryAlpha:
    r"""\<颜色序号>a[&][H]<AA>[&]"""

    # "<AA> 是一个十六进制的透明度数值，00 为全见，FF 为全透明。"
    # "<颜色序号> 含义同上，但这里不能省略。写法举例：\1a&H80&、\2a&H80、\3a80、\4a&H80&。"
    # "其中的 & 和 H 按规范应该是要有的，但是如果没有也能正常解析。"
    # Annotations 文本好像没有透明度, 这个很符合直觉
    def __init__(self, alpha: Alpha):
        self.alpha = alpha

    def __str__(self) -> str:
        def DumpAlpha(alpha: Alpha) -> str:
            # 据 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 所说
            # SSA 的 Alpha 是透明度, 00 为不透明，FF 为全透明
            return "&H{:02X}&".format(255 - alpha.alpha)

        return rf"\1a{DumpAlpha(self.alpha)}"


class Bold:
    r"""\b<0 或 1>"""

    # "\b1 把文本变为粗体，\b0 强制文本不是粗体。"
    def __init__(self, bold: float):
        self.bold = bold

    def __str__(self) -> str:
        return rf"\b{self.bold}"


class Bord:
    r"""\bord<宽度>"""

    # "边框宽度，为像素，可以是小数。"
    def __init__(self, bord: float):
        self.bord = bord

    def __str__(self) -> str:
        return rf"\bord{self.bord}"


class Shadow:
    r"""\shad<深度>"""

    # "阴影深度，为像素，可以是小数。"
    def __init__(self, shadow: float):
        self.shadow = shadow

    def __str__(self) -> str:
        return rf"\shad{self.shadow}"


class iClip:
    r"""\iclip((<x1>,<y1>,<x2>,<y2>))"""

    # "定义一个矩形，只有在该矩形范围内的内容不可见。"
    # "<x1>,<y1> 为矩形的左上角，<x2>,<y2> 为矩形的右下角。"
    # "当一行中有多个 \[i]clip 时，以__最后一个__为准。"
    def __init__(self, x: float, y: float, x1: float, y1: float):
        self.x = _round(x)
        self.y = _round(y)
        self.x1 = _round(x1)
        self.y1 = _round(y1)

    def __str__(self) -> str:
        return rf"\iclip({self.x},{self.y},{self.x1},{self.y1})"
