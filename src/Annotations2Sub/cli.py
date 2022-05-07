#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import defusedxml.ElementTree  # type: ignore

from Annotations2Sub.Annotation import Parse
from Annotations2Sub.Convert import Convert
from Annotations2Sub.Sub import Sub
from Annotations2Sub.locale import _


def main():
    parser = argparse.ArgumentParser(
        description=_("一个可以把Youtube注释转换成ASS字幕(Sub Station Alpha V4)文件的脚本")
    )
    parser.add_argument(
        "File",
        type=str,
        nargs="+",
        metavar=_("文件 或 视频ID"),
        help=_("多个需要转换的文件或者是需要预览或生成 Youtube 视频的 videoId"),
    )
    parser.add_argument(
        "-l", "--embrace-libass", action="store_true", help=_("拥抱 libass 的怪癖")
    )
    parser.add_argument(
        "-x",
        "--transform-resolution-x",
        default=100,
        type=int,
        metavar=100,
        help=_("变换分辨率X"),
    )
    parser.add_argument(
        "-y",
        "--transform-resolution-y",
        default=100,
        type=int,
        metavar=100,
        help=_("变换分辨率Y"),
    )
    parser.add_argument(
        "-f", "--font", default="Microsoft YaHei", type=str, metavar="Microsoft YaHei", help=_("指定字体")
    )
    args = parser.parse_args()
    file = args.File[0]
    string = open(file, "r", encoding="utf-8").read()
    tree = defusedxml.ElementTree.fromstring(string)
    annotations = Parse(tree)
    events = Convert(
        annotations,
        args.embrace_libass,
        args.transform_resolution_x,
        args.transform_resolution_y,
    )
    sub = Sub()
    sub.events.events.extend(events)
    sub.info.info["PlayResX"] = args.transform_resolution_x
    sub.info.info["PlayResY"] = args.transform_resolution_y
    sub.events.events.sort(key=lambda event: event.Start)
    sub.styles.styles["Default"].Fontname = args.font
    s = sub.Dump()
    with open(file + ".ass", "w", encoding="utf-8") as f:
        f.write(s)
