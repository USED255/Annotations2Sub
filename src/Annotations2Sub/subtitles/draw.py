from Annotations2Sub.subtitles.utils import Literal, _round


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
        return "".join(map(str, self))
