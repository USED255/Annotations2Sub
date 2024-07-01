import os
import xml.etree.ElementTree

from Annotations2Sub._Convert import Convert
from Annotations2Sub._Sub import Sub
from Annotations2Sub.Annotations import NotAnnotationsDocumentError, Parse
from Annotations2Sub.i18n import _


def AnnotationsXmlFileToSubtitleFile(
    annotations_file: str,
    output_file: str,
    transform_resolution_x: int = 100,
    transform_resolution_y: int = 100,
    font="Microsoft YaHei",
):
    if os.path.isfile(annotations_file) is False:
        raise FileNotFoundError(_("{} 不是一个文件").format(annotations_file))

    with open(annotations_file, "r", encoding="utf-8") as f:
        annotations_string = f.read()

    subtitle_string = AnnotationsXmlStringToSubtitleString(
        annotations_string,
        transform_resolution_x,
        transform_resolution_y,
        font,
        os.path.basename(annotations_file),
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(subtitle_string)


def AnnotationsXmlStringToSubtitleString(
    annotations_string: str,
    transform_resolution_x: int = 100,
    transform_resolution_y: int = 100,
    font=_("Microsoft YaHei"),
    title=_("无标题"),
) -> str:

    tree = xml.etree.ElementTree.fromstring(annotations_string)
    annotations = Parse(tree)

    events = Convert(
        annotations,
        transform_resolution_x,
        transform_resolution_y,
    )

    # Annotations 是无序的
    # 按时间重新排列字幕事件, 是为了人类可读
    events.sort(key=lambda event: event.Start)

    subtitle = Sub()
    subtitle.comment += _("此脚本使用 Annotations2Sub 生成") + "\n"
    subtitle.comment += "https://github.com/USED255/Annotations2Sub"
    subtitle.info["Title"] = os.path.basename(title)
    subtitle.info["PlayResX"] = str(transform_resolution_x)
    subtitle.info["PlayResY"] = str(transform_resolution_y)
    subtitle.info["WrapStyle"] = "2"
    subtitle.styles["Default"].Fontname = font
    subtitle.events.extend(events)
    return subtitle.Dump()
