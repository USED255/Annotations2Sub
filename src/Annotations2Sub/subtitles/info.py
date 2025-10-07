# -*- coding: utf-8 -*-

from Annotations2Sub.subtitles.CONSTANT import InfoHEAD


# class Info(dict[str, str]):
class Info(dict):
    """SSA 的信息(Info) 结构"""

    def __init__(self):
        # 必要的字段
        self["ScriptType"] = "v4.00+"

    def __str__(self) -> str:
        def f2(item) -> str:
            k, v = item
            return f"{k}: {v}\n"

        info_string = "".join(map(f2, self.items())) + "\n"

        return InfoHEAD + info_string
