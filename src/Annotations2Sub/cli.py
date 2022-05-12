#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
import traceback
import urllib.request
import defusedxml.ElementTree  # type: ignore
import _thread

from Annotations2Sub import version
from Annotations2Sub.flag import Flags
from Annotations2Sub.Annotation import Parse
from Annotations2Sub.Convert import Convert
from Annotations2Sub.Sub import Sub
from Annotations2Sub.internationalization import _
from Annotations2Sub.tools import (
    AnnotationsForArchive,
    CheckUrl,
    RedText,
    VideoForInvidiou,
    YellowText,
)


def main():
    parser = argparse.ArgumentParser(
        description=_(
            "一个可以把 Youtube Annotation 转换成 ASS 字幕(Advanced SubStation Alpha)文件的脚本"
        )
    )
    parser.add_argument(
        "queue",
        type=str,
        nargs="+",
        metavar=_("文件 或 videoId"),
        help=_(
            "多个需要转换的文件的文件路径, 或者是多个需要预览, 生成, 从Internet Archive 下载注释文件 Youtube 视频的 videoId"
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
        type=str,
        metavar=_("文件夹"),
        help=_("指定转换后文件的输出路径, 不指定此选项转换后的文件会输出至与被转换文件同一目录"),
    )
    parser.add_argument(
        "-d",
        "--download-for-archive",
        action="store_true",
        help=_("尝试从 Internet Archive 下载注释文件"),
    )
    parser.add_argument(
        "-i",
        "--invidious-instances",
        metavar="invidious.domain",
        help=_("指定 invidious 实例(https://redirect.invidious.io/)"),
    )
    parser.add_argument(
        "-p",
        "--preview-video",
        action="store_true",
        help=_("预览视频, 需要 mpv(https://mpv.io/) 并指定 invidious 实例"),
    )
    parser.add_argument(
        "-g",
        "--generate-video",
        action="store_true",
        help=_("生成视频, 需要 FFmpeg(https://ffmpeg.org/) 并指定 invidious 实例)"),
    )
    parser.add_argument(
        "-u",
        "--unstable",
        action="store_true",
        help=_("启用不稳定功能, 会出现一些问题"),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help=_("显示版本号"),
    )
    parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        help=_("显示更多些消息"),
    )
    args = parser.parse_args()

    filePaths = []

    if args.version:
        print(_("Annotations2Sub v{version}").format(version=version))
        return

    if args.unstable:
        Flags.unstable = True

    if args.verbose:
        Flags.verbose = True

    if args.output_path != None:
        if os.path.isfile(args.output_path):
            print(RedText(_("转换后文件的输出路径应该指定一个文件夹, 而不是文件")))
            exit(1)

    if args.preview_video or args.generate_video:
        if args.invidious_instances is None:
            print(RedText(_("请指定一个 invidious 实例")))
            print(_("你可以在这里找一个:"),"https://redirect.invidious.io/")
            exit(1)
        args.download_for_archive = True
        args.embrace_libass = True

    if args.download_for_archive is False:
        for filePath in args.queue:
            if os.path.isfile(filePath) is False:
                print(RedText(_("{} 不是一个文件").format(filePath)))
                exit(1)
            try:
                tree = defusedxml.ElementTree.parse(filePath)
                count = 0
                for each in tree.find("annotations").findall("annotation"):
                    count += 1
                if count == 0:
                    print(RedText(_("{} 没有 Annotation").format(filePath)))
                    exit(1)
            except:
                print(RedText(_("{} 不是一个有效的 XML 文件").format(filePath)))
                print(traceback.format_exc())
                exit(1)
            filePaths.append(filePath)

    if args.download_for_archive:

        def CheckNetwork():
            if CheckUrl() is False:
                print(YellowText(_("您好像无法访问 Google 🤔")))

        _thread.start_new_thread(CheckNetwork, ())

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
                print(YellowText(_("{} 可能没有 Annotation").format(videoId)))
                continue
            with open(filePath, "w", encoding="utf-8") as f:
                f.write(string)
            filePaths.append(filePath)

    if args.embrace_libass and (
        args.transform_resolution_x == 100 or args.transform_resolution_y == 100
    ):
        print(
            YellowText(
                _(
                    "--embrace-libass 需要注意, 如果您的视频不是 16:9, 请使用 --transform-resolution-x --transform-resolution-y, 以确保效果."
                )
            )
        )

    outputs = []
    for filePath in filePaths:
        output = filePath + ".ass"
        if args.output_path != None:
            fileName = os.path.basename(filePath) + ".ass"
            output = os.path.join(args.output_path, fileName)

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
        if events == []:
            print(YellowText(_("{} 没有注释被转换").format(filePath)))
        events.sort(key=lambda event: event.Start)
        sub = Sub()
        sub.events.extend(events)
        sub.info["PlayResX"] = args.transform_resolution_x
        sub.info["PlayResY"] = args.transform_resolution_y
        sub.info["Title"] = filePath
        sub.styles["Default"].Fontname = args.font
        subString = sub.Dump()
        with open(output, "w", encoding="utf-8") as f:
            f.write(subString)
        print(_("保存于: {}").format(output))
        outputs.append(output)

    if args.preview_video:
        for output in outputs:
            video, audio = VideoForInvidiou(videoId, args.invidious_instances)
            cmd = rf'mpv "{video}" --audio-file="{audio}" --sub-file="{output}"'
            if Flags.verbose:
                print(cmd)
            exit_code = os.system(cmd)
            if Flags.verbose:
                if exit_code != 0:
                    print(YellowText("exit with {}".format(exit_code)))

    if args.generate_video:
        for output in outputs:
            video, audio = VideoForInvidiou(videoId, args.invidious_instances)
            cmd = rf'ffmpeg -i "{video}" -i "{audio}" -vf "ass={output}" {output}.mp4'
            if Flags.verbose:
                print(cmd)
            exit_code = os.system(cmd)
            if Flags.verbose:
                if exit_code != 0:
                    print(YellowText("exit with {}".format(exit_code)))
