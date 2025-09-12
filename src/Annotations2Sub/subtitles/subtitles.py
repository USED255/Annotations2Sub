# -*- coding: utf-8 -*-

"""SSA 相关"""

from Annotations2Sub.subtitles.event import Events
from Annotations2Sub.subtitles.info import Info
from Annotations2Sub.subtitles.style import Style, Styles


class Subtitles:
    """SSA 类"""

    def __init__(self):
        self.info = Info()
        self.styles = Styles()
        self.events = Events()

        # 通常脚本中会有一些注释写了谁生成了这个脚本
        self.comment = ""
        """ 脚本注释 """

        # "标题，对脚本的描述。如果未指定，自动设置为 <untitled>。"
        self.info["Title"] = "Default File"

    def __str__(self) -> str:
        self.info.comment = self.comment
        return str(self.info) + str(self.styles) + str(self.events)

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, value: object) -> bool:
        return str(self) == str(value)
