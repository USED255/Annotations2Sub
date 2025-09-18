# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree

from Annotations2Sub.Annotations import Parse
from Annotations2Sub.convert import Convert
from Annotations2Sub.i18n import _
from Annotations2Sub.subtitles import Subtitles
from Annotations2Sub.utils import Warn


class AnnotationsStringIsEmptyError(ValueError):
    pass


def AnnotationsXmlStringToSubtitlesString(
    annotations_string: str,
    transform_resolution_x: int = 100,
    transform_resolution_y: int = 100,
    font=_("Microsoft YaHei"),
    title=_("无标题"),
) -> str:

    if annotations_string == "":
        raise AnnotationsStringIsEmptyError(_("annotations_string 不应为空字符串"))

    tree = xml.etree.ElementTree.fromstring(annotations_string)
    annotations = Parse(tree)

    events = Convert(
        annotations,
        transform_resolution_x,
        transform_resolution_y,
    )

    if events == []:
        Warn(_('"{}" 没有注释被转换').format(title))

    # Annotations 是无序的
    # 按时间重新排列字幕事件, 是为了人类可读
    events.sort(key=lambda event: event.Start)

    subtitles = Subtitles()
    subtitles.comment += _("此脚本使用 Annotations2Sub 生成") + "\n"
    subtitles.comment += "https://github.com/USED255/Annotations2Sub"
    subtitles.info["Title"] = os.path.basename(title)
    subtitles.info["PlayResX"] = str(transform_resolution_x)
    subtitles.info["PlayResY"] = str(transform_resolution_y)
    subtitles.info["WrapStyle"] = "2"
    subtitles.styles["Default"].Fontname = font
    subtitles.events.extend(events)

    return str(subtitles)
