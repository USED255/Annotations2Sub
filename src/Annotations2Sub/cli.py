#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import defusedxml.ElementTree  # type: ignore

from Annotations2Sub.Annotation import Parse
from Annotations2Sub.Convert import Convert
from Annotations2Sub.Sub import Sub
from Annotations2Sub.locale import _


def YellowText(s: str) -> str:
    return "\033[33m" + s + "\033[0m"


def RedText(s: str) -> str:
    return "\033[31m" + s + "\033[0m"


def main():
    parser = argparse.ArgumentParser(
        description=_("一个可以把Youtube注释转换成ASS字幕(Sub Station Alpha V4)文件的脚本")
    )
    parser.add_argument(
        "queue",
        type=str,
        nargs="+",
        metavar=_("文件 或 视频ID"),
        help=_("多个需要转换的文件或者是需要预览或生成 Youtube 视频的 videoId"),
    )
    parser.add_argument(
        "-l",
        "--embrace-libass",
        action="store_true",
        help=_("拥抱 libass 的怪癖和特性, 不指定此选项则会适配 xy-vsfilter"),
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
        "-f",
        "--font",
        default="Microsoft YaHei",
        type=str,
        metavar="Microsoft YaHei",
        help=_("指定字体"),
    )
    parser.add_argument(
        "-o",
        "--output-path",
        default=None,
        type=str,
        metavar="文件",
        help=_("指定转换后文件的输出路径, 不指定此选项会转换后的文件输出至与被转换文件同一目录"),
    )
    args = parser.parse_args()

    if args.output_path != None:
        output_path = os.path.abspath(args.output_path)
        if os.path.isfile(output_path):
            print(RedText(_("转换后文件的输出路径应该指定一个文件夹, 而不是文件")))
            exit(1)

    for filePath in args.queue:
        if os.path.isfile(filePath) == False:
            print(RedText(_("{} 不是一个文件").format(filePath)))
            exit(1)
        with open(filePath, "r", encoding="utf-8") as f:
            string = f.read()
        tree = defusedxml.ElementTree.fromstring(string)
        annotations = Parse(tree)
        events = Convert(
            annotations,
            args.embrace_libass,
            args.transform_resolution_x,
            args.transform_resolution_y,
        )
        events.sort(key=lambda event: event.Start)
        sub = Sub()
        sub.events.events.extend(events)
        sub.info.info["PlayResX"] = args.transform_resolution_x
        sub.info.info["PlayResY"] = args.transform_resolution_y
        sub.styles.styles["Default"].Fontname = args.font
        subString = sub.Dump()

        fileName = os.path.basename(filePath) + ".ass"
        output = os.path.join(args.output_path, fileName)
        with open(output, "w", encoding="utf-8") as f:
            f.write(subString)
