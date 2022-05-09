#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import asyncio
import os
import re
import traceback
import urllib.request
import defusedxml.ElementTree  # type: ignore

from Annotations2Sub.Annotation import Parse
from Annotations2Sub.Convert import Convert
from Annotations2Sub.Sub import Sub
from Annotations2Sub.locale import _
from Annotations2Sub.tools import AnnotationsForArchive, CheckUrl, RedText, YellowText


def main():
    def convert():
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

        with open(output, "w", encoding="utf-8") as f:
            f.write(subString)
        print(_("保存于: {}").format(output))

    def CheckNetwork():
        async def checkNetwork():
            if CheckUrl() is False:
                print(YellowText(_("您好像无法访问 Google 🤔")))
                print(YellowText(_("请检查您的网络连接")))

        asyncio.run(checkNetwork())

    parser = argparse.ArgumentParser(
        description=_("一个可以把 Youtube Annotations 转换成 ASS 字幕(Sub Station Alpha V4)文件的脚本")
    )
    parser.add_argument(
        "queue",
        type=str,
        nargs="+",
        metavar=_("文件 或 videoId"),
        help=_(
            "多个需要转换的文件的文件路径, 或者是多个需要预览, 生成, 从Internet Archive 下载 Annotations 文件 Youtube 视频的 videoId"
        ),
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
        default=_("Microsoft YaHei"),
        type=str,
        metavar=_("Microsoft YaHei"),
        help=_("指定字体"),
    )
    parser.add_argument(
        "-o",
        "--output-path",
        default=None,
        type=str,
        metavar=_("文件夹"),
        help=_("指定转换后文件的输出路径, 不指定此选项转换后的文件会输出至与被转换文件同一目录"),
    )
    parser.add_argument(
        "-d",
        "--download-for-archive",
        action="store_true",
        help=_("尝试从 Internet Archive 下载 Annotations 文件"),
    )
    args = parser.parse_args()

    filePaths = []

    if args.output_path != None:
        if os.path.isfile(args.output_path):
            print(RedText(_("转换后文件的输出路径应该指定一个文件夹, 而不是文件")))
            exit(1)
    if args.download_for_archive is False:
        for filePath in args.queue:
            if os.path.isfile(filePath) is False:
                print(RedText(_("{} 不是一个文件").format(filePath)))
                exit(1)
            try:
                defusedxml.ElementTree.parse(filePath)
            except:
                print(RedText(_("{} 不是一个有效的 XML 文件").format(filePath)))
                print(traceback.format_exc())
                exit(1)
            filePaths.append(filePath)

    if args.download_for_archive:
        CheckNetwork()
        videoIds = []
        for videoId in args.queue:
            if re.match(r"[a-zA-Z0-9_-]{11}", videoId) is None:
                raise ValueError("Invalid videoId")
            videoIds.append(videoId)
        for videoId in videoIds:
            filePath = f"{videoId}.xml"
            if args.output_path != None:
                filePath = os.path.join(args.output_path, filePath)
            url = AnnotationsForArchive(videoId)
            print(_("下载 {}").format(url))
            string = urllib.request.urlopen(url).read().decode("utf-8")
            if string == "":
                print(YellowText(_("{} 可能没有 Annotations").format(videoId)))
                continue
            with open(filePath, "w", encoding="utf-8") as f:
                f.write(string)
            filePaths.append(filePath)

    for filePath in filePaths:
        output = filePath + ".ass"
        if args.output_path != None:
            fileName = os.path.basename(filePath) + ".ass"
            output = os.path.join(args.output_path, fileName)
        convert()
