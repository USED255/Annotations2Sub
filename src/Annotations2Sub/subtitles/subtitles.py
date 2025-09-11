# -*- coding: utf-8 -*-

"""SSA 相关"""

from Annotations2Sub.subtitles.event import Events
from Annotations2Sub.subtitles.info import Info
from Annotations2Sub.subtitles.style import Style, Styles


class Subtitles:
    """SSA 类"""

    def __init__(self):
        self._info = Info()
        self._styles = Styles()
        self._events = Events()

        self.info = self._info.infos
        """ 脚本配置 """

        # 通常脚本中会有一些注释写了谁生成了这个脚本
        self.comment = ""
        """ 脚本注释 """

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
