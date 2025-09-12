from Annotations2Sub.subtitles.CONSTANT import InfoHEAD


# class Info(dict[str, str]):
class Info(dict):
    """SSA 的信息(Info) 结构"""

    def __init__(self):
        # 好像流行开头来一段注释的样子
        self.comment: str = ""
        # 必要的字段
        self["ScriptType"] = "v4.00+"

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
        info_string = "".join(map(f2, self.items())) + "\n"

        return InfoHEAD + comment_string + info_string
