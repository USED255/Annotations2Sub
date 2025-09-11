from typing import Dict

from Annotations2Sub.color import Alpha, Color, Rgba
from Annotations2Sub.subtitles.CONSTANT import StylesHEAD
from Annotations2Sub.subtitles.utils import Literal


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
        def DumpABGR(rgba: Rgba) -> str:
            # "长整型 BGR（蓝绿红）值，还包含了 alpha 通道信息。"
            # "该值的十六进制字节顺序为 AABBGGRR。例如，&H00FFFFFF。"
            return "&H{:02X}{:02X}{:02X}{:02X}".format(
                rgba.alpha, rgba.blue, rgba.green, rgba.red
            )

        return f"Style: {{}},{self.Fontname},{self.Fontsize},{DumpABGR(self.PrimaryColour)},{DumpABGR(self.SecondaryColour)},{DumpABGR(self.OutlineColour)},{DumpABGR(self.BackColour)},{self.Bold},{self.Italic},{self.Underline},{self.StrikeOut},{self.ScaleX},{self.ScaleY},{self.Spacing},{self.Angle},{self.BorderStyle},{self.Outline},{self.Shadow},{self.Alignment},{self.MarginL},{self.MarginR},{self.MarginV},{self.Encoding}\n"


class Styles:
    def __init__(self):
        self.styles: Dict[str, Style] = {}

    def __str__(self) -> str:
        # def f(item: tuple[str, Style]) -> str:
        def f(item) -> str:
            Name = item[0]
            StyleString = str(item[1])

            return StyleString.format(Name)

        string = "\n".join(map(f, self.styles.items())) + "\n"

        return StylesHEAD + string
