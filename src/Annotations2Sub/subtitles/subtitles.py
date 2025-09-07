# -*- coding: utf-8 -*-

"""SSA 相关"""

from typing import Dict, List

from Annotations2Sub.subtitles.CONSTANT import EventsHEAD, InfoHEAD, StylesHEAD
from Annotations2Sub.subtitles.event import Event
from Annotations2Sub.subtitles.style import Style


class Subtitles:
    """SSA 类"""

    def __init__(self):
        self._info = self._Info()
        self._styles = self._Styles()
        self._events = self._Events()

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

    class _Info:
        """SSA 的信息(Info) 结构"""

        def __init__(self):
            # 好像流行开头来一段注释的样子
            self.comment: str = ""
            # 必要的字段
            self.infos: Dict[str, str] = {"ScriptType": "v4.00+"}

        def __str__(self) -> str:
            def f1(line: str) -> str:
                if line == "":
                    return ""
                return f"; {line}\n"

            def f2(item) -> str:
                k, v = item
                return f"{k}: {v}\n"

            comment_lines = self.comment.split("\n")
            comment_string = "".join(map(f1, comment_lines))
            info_string = "".join(map(f2, self.infos.items())) + "\n"

            return InfoHEAD + comment_string + info_string

    class _Styles:
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

    class _Events:
        def __init__(self):
            self.events: List[Event] = []

        def __str__(self) -> str:
            string = "".join(map(str, self.events)) + "\n"
            return EventsHEAD + string
