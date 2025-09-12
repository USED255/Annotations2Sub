from datetime import datetime

from Annotations2Sub.subtitles.CONSTANT import EventsHEAD
from Annotations2Sub.subtitles.utils import Literal


class Event:
    """SSA 事件(Event) 结构"""

    def __init__(self):
        # 有 Dialogue, Comment, Picture, Sound, Movie, Command 事件,
        # 只用到了 Dialogue.
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
            # "格式为 0:00:00:00（小时:分:秒:毫秒）"
            return time.strftime("%H:%M:%S.%f")[:-4]

        return f"{self.Type}: {self.Layer},{DumpTime(self.Start)},{DumpTime(self.End)},{self.Style},{self.Name},{self.MarginL},{self.MarginR},{self.MarginV},{self.Effect},{self.Text}\n"


# class Events(list[Event]):
class Events(list):
    def __str__(self) -> str:
        string = "".join(map(str, self)) + "\n"
        return EventsHEAD + string
