# -*- coding: utf-8 -*-

"""SSA 相关"""

from datetime import datetime
from typing import Dict, List

from Annotations2Sub.Color import Alpha, Color, Rgba

# 兼容 Python3.6, 3.7
# Python3.6, 3.7 的 typing 没有 Literal
try:
    from typing import Literal
except ImportError:

    class a:
        def __getitem__(self, b):
            return b

    exec("Literal = a()")

accuracy = 3


def _round(x: float) -> float:
    return round(x, accuracy)


class Style:
    """SSA 样式(Style) 结构"""

    def __init__(self):
        # 带引号的是从 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 粘过来的
        # Name 不在这里, 它会这样出现 Dict[Name:str, Style:Style]

        # "Style 行中的所有设定，除了阴影和边框的类型和深度，都可以被字幕文本中的控制代码所覆写。"
        # "使用的字体名称，区分大小写。"
        self.Fontname: str = "Arial"

        # 本项目的样式都用样式复写标签实现, 这些字段不会用到
        self.Fontsize: float = 20
        self.PrimaryColour: Rgba = Rgba(Color(255, 255, 255), Alpha(0))
        self.SecondaryColour: Rgba = Rgba(Color(255, 0, 0), Alpha(0))
        self.OutlineColour: Rgba = Rgba(Color(0, 0, 0), Alpha(0))
        self.BackColour: Rgba = Rgba(Color(0, 0, 0), Alpha(0))
        self.Bold: Literal[-1, 0] = 0
        self.Italic: Literal[-1, 0] = 0
        self.Underline: Literal[-1, 0] = 0
        self.StrikeOut: Literal[-1, 0] = 0
        self.ScaleX: int = 100
        self.ScaleY: int = 100
        self.Spacing: int = 0
        self.Angle: float = 0
        self.BorderStyle: Literal[1, 3] = 1
        self.Outline: Literal[0, 1, 2, 3, 4] = 2
        self.Shadow: Literal[0, 1, 2, 3, 4] = 2
        self.Alignment: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = 2
        self.MarginL: int = 10
        self.MarginR: int = 10
        self.MarginV: int = 10

        # "它定义了字体的字符集或编码方式。"
        # "在多语种的 Windows 安装中它可以获取多种语言中的字符。"
        # "通常 0 为英文，134 为简体中文，136 为繁体中文。"
        # "当文件是 Unicode 编码时，该字段在解析对话时会起作用。"
        # 直接抄 Aegisub 置为 1
        self.Encoding: int = 1

    def __str__(self) -> str:
        def DumpAABBGGRR(rgba: Rgba) -> str:
            """转换为 SSA 颜色字符串"""

            # "长整型 BGR（蓝绿红）值，还包含了 alpha 通道信息。"
            # "该值的十六进制字节顺序为 AABBGGRR。例如，&H00FFFFFF。"
            return "&H{:02X}{:02X}{:02X}{:02X}".format(
                rgba.alpha, rgba.blue, rgba.green, rgba.red
            )

        return f"Style: {{}},{self.Fontname},{self.Fontsize},{DumpAABBGGRR(self.PrimaryColour)},{DumpAABBGGRR(self.SecondaryColour)},{DumpAABBGGRR(self.OutlineColour)},{DumpAABBGGRR(self.BackColour)},{self.Bold},{self.Italic},{self.Underline},{self.StrikeOut},{self.ScaleX},{self.ScaleY},{self.Spacing},{self.Angle},{self.BorderStyle},{self.Outline},{self.Shadow},{self.Alignment},{self.MarginL},{self.MarginR},{self.MarginV},{self.Encoding}\n"


class Event:
    """SSA 事件(Event) 结构"""

    def __init__(self):
        # 有 Dialogue, Comment, Picture, Sound, Movie, Command 事件
        # 只用到了 Dialogue
        # "这是一个对话事件，即显示一些文本。"
        self.Type: Literal["Dialogue"] = "Dialogue"
        # Aegisub 没有 Marked, 所以我们也没有
        self.Layer: int = 0
        self.Start: datetime = datetime.strptime("0", "%S")
        self.End: datetime = datetime.strptime("0", "%S")
        self.Style: str = "Default"
        self.Name: str = ""
        # MarginL, MarginR, MarginV, Effect 在本项目中均没有使用
        self.MarginL: int = 0
        self.MarginR: int = 0
        self.MarginV: int = 0
        self.Effect: str = ""
        self.Text: str = ""

    def __str__(self) -> str:
        def DumpTime(time: datetime) -> str:
            """转换为 SSA 时间字符串"""

            # "格式为 0:00:00:00（小时:分:秒:毫秒）"
            return time.strftime("%H:%M:%S.%f")[:-4]

        return f"{self.Type}: {self.Layer},{DumpTime(self.Start)},{DumpTime(self.End)},{self.Style},{self.Name},{self.MarginL},{self.MarginR},{self.MarginV},{self.Effect},{self.Text}\n"


class Sub:
    """SSA 类"""

    def __init__(self):
        self._info = self._Info()
        self._styles = self._Styles()
        self._events = self._Events()

        self.info = self._info.infos
        """ 这个结构中会有一些脚本的配置 """

        self.comment = ""
        """ 通常脚本中会有一些注释写了谁生成了这个脚本 """

        self.styles = self._styles.styles
        self.events = self._events.events

        # "标题，对脚本的描述。如果未指定，自动设置为 <untitled>。"
        self.info["Title"] = "Default File"
        # 定义默认样式
        self.styles["Default"] = Style()

    def __str__(self) -> str:
        self._info.comment = self.comment

        string = ""
        string += str(self._info)
        string += str(self._styles)
        string += str(self._events)
        return string

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, value: object) -> bool:
        return str(self) == str(value)

    def Dump(self) -> str:
        """转储为 SSA"""
        return str(self)

    class _Info:
        """SSA 的信息(Info) 结构"""

        def __init__(self):
            # 好像流行开头来一段注释的样子
            self.comment: str = ""
            # 必要的字段
            self.infos: Dict[str, str] = {"ScriptType": "v4.00+"}

        def __str__(self) -> str:
            # 只是暴力拼接字符串而已
            string = ""
            string += "[Script Info]\n"
            if self.comment != "":
                for line in self.comment.split("\n"):
                    string += f"; {line}\n"
            for k, v in self.infos.items():
                string += f"{k}: {v}\n"
            string += "\n"
            return string

    class _Styles:
        def __init__(self):
            self.styles: Dict[str, Style] = {}

        def __str__(self) -> str:
            string = ""
            string += "[V4+ Styles]\n"
            string += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"

            for Name, Styles in self.styles.items():
                string += str(Styles).format(Name)
            string += "\n"
            return string

    class _Events:
        def __init__(self):
            self.events: List[Event] = []

        def __str__(self) -> str:
            string = ""
            string += "[Events]\n"
            string += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

            for event in self.events:
                string += str(event)
            string += "\n"
            return string


class DrawCommand:
    """绘图指令结构"""

    def __init__(self, x: float = 0, y: float = 0, command: Literal["m", "l"] = "m"):
        self.x: float = _round(x)
        self.y: float = _round(y)
        # 命令有 m, n, l, b, s, p, c
        # 这里仅列出需要的命令
        self.command: Literal["m", "l"] = command

    def __str__(self) -> str:
        return f"{self.command} {self.x} {self.y} "


class Draw(list):
    def __str__(self) -> str:
        # "所有绘图都应由 m <x> <y> 命令开头"
        # "所有没闭合的图形会被自动地在起点和终点之间添加直线来闭合。"
        # "如果一个对话行中的多个图形有重叠，重叠部分会进行异或运算。"
        string = ""
        for draw in self:
            string += str(draw)
        return string


def DumpColor(color: Color) -> str:
    """将 Color 转换为 SSA 的颜色表示"""
    return "&H{:02X}{:02X}{:02X}&".format(color.red, color.green, color.blue)


def DumpAlpha(alpha: Alpha) -> str:
    """将 Alpha 转换为 SSA 的 Alpha 表示"""

    # 据 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 所说
    # SSA 的 Alpha 是透明度, 00 为不透明，FF 为全透明
    return "&H{:02X}&".format(255 - alpha.alpha)


class Tag(list):
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
            return rf"\fs{str(self.size)}"

    class PrimaryColour:
        r"""\<颜色序号>c[&][H]<BBGGRR>[&]"""

        # "<BBGGRR> 是一个十六进制的 RGB 值，但颜色顺序相反，前导的 0 可以省略。"
        # "<颜色序号> 可选值为 1、2、3 和 4，分别对应单独设置 PrimaryColour、SecondaryColour、OutlineColor 和 BackColour"
        # "其中的 & 和 H 按规范应该是要有的，但是如果没有也能正常解析。"
        # PrimaryColour 填充颜色, SecondaryColour 卡拉OK变色, OutlineColor 边框颜色, BackColour 阴影颜色
        def __init__(self, colour: Color):
            self.colour = colour

        def __str__(self) -> str:
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
