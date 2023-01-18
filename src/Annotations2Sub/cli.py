#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import _thread
import argparse
import os
import re
import sys
import traceback
import urllib.request

# 我觉得在输入确定的环境下用不着这玩意
# 不过打包到了 PyPI 也不用像以前那些忌惮第三方库了
# 不用白不用
import defusedxml.ElementTree  # type: ignore

from Annotations2Sub import version
from Annotations2Sub.Annotation import Parse
from Annotations2Sub.Convert import Convert
from Annotations2Sub.Sub import Sub
from Annotations2Sub.tools import (
    AnnotationsForArchive,
    CheckUrl,
    RedText,
    Stderr,
    VideoForInvidious,
    YellowText,
    _,
    Flags,
)


def run():
    """程序入口"""
    parser = argparse.ArgumentParser(description=_("下载和转换 Youtube 注释"))
    parser.add_argument(
        "queue",
        nargs="+",
        type=str,
        metavar=_("文件 或 videoId"),
        help=_("多个需要转换的文件的文件路径或视频ID"),
    )
    parser.add_argument(
        "-l",
        "--embrace-libass",
        action="store_true",
        help=_("拥抱 libass 的怪癖和特性, 不指定此选项则会适配 xy-vsfilter"),
    )

    # 虽然把分辨率置为 100, 100 字幕滤镜也能正常定位, 但是显然正确的分辨率更惹字幕滤镜喜欢
    parser.add_argument(
        "-x",
        "--transform-resolution-x",
        default=100,
        type=int,
        metavar="100",
        help=_("变换分辨率X"),
    )
    parser.add_argument(
        "-y",
        "--transform-resolution-y",
        default=100,
        type=int,
        metavar="100",
        help=_("变换分辨率Y"),
    )

    # 应该使用非衬线字体, 但是 SSA 不能方便的指定字体家族, 只得出此下策
    parser.add_argument(
        "-f",
        "--font",
        default=_("Microsoft YaHei"),
        type=str,
        metavar=_("Microsoft YaHei"),
        help=_("指定字体"),
    )
    parser.add_argument(
        "-d",
        "--download-for-archive",
        action="store_true",
        help=_("尝试从 Internet Archive 下载注释文件"),
    )
    parser.add_argument(
        "-D",
        "--download-annotation-only",
        action="store_true",
        help=_("仅下载注释"),
    )
    # 就是拼接参数执行 mpv
    parser.add_argument(
        "-p",
        "--preview-video",
        action="store_true",
        help=_("预览视频, 需要 mpv(https://mpv.io/)"),
    )

    # 与上面同理
    parser.add_argument(
        "-g",
        "--generate-video",
        action="store_true",
        help=_("生成视频, 需要 FFmpeg(https://ffmpeg.org/)"),
    )
    parser.add_argument(
        "-i",
        "--invidious-instances",
        type=str,
        metavar="invidious.domain",
        help=_("指定 invidious 实例(https://redirect.invidious.io/)"),
    )

    # 与 Unix 工具结合成为了可能
    parser.add_argument(
        "-s", "--output-to-stdout", action="store_true", help=_("输出至标准输出")
    )
    parser.add_argument(
        "-n", "--no-overwrite-files", action="store_true", help=_("不覆盖文件")
    )

    # 指从 Internet Archive 下载的注释文件
    parser.add_argument(
        "-N", "--no-keep-intermediate-files", action="store_true", help=_("不保留中间文件")
    )

    parser.add_argument(
        "-o",
        "--output-directory",
        type=str,
        metavar=_("目录"),
        help=_("指定转换后文件的输出目录"),
    )
    parser.add_argument("-O", "--output", type=str, metavar=_("文件"), help=_("保存到此文件"))
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help=_("显示版本号"),
        version=_("Annotations2Sub v{version}").format(version=version),
    )

    # 这个不是用来调试用的
    parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        help=_("显示更多消息"),
    )

    args = parser.parse_args()

    if args.verbose:
        Flags.verbose = True

    if args.output_to_stdout:
        if args.output_directory is not None:
            Stderr(RedText(_("--output-to-stdout 不能与 --output-directory 选项同时使用")))
            exit(1)
        if args.no_overwrite_files:
            Stderr(RedText(_("--output-to-stdout 不能与 --no-overwrite-files 选项同时使用")))
            exit(1)
        if args.output is not None:
            Stderr(RedText(_("--output-to-stdout 不能与 --output 选项同时使用")))
            exit(1)
        if args.download_annotation_only:
            Stderr(
                RedText(_("--output-to-stdout 不能与 --download-annotation-only 选项同时使用"))
            )
            exit(1)
        if args.preview_video or args.generate_video:
            Stderr(
                RedText(
                    _(
                        "--output-to-stdout 不能与 --preview-video 或 --generate-video 选项同时使用"
                    )
                )
            )
            exit(1)

    if args.no_keep_intermediate_files:
        if args.download_annotation_only:
            Stderr(
                RedText(
                    _(
                        "--no-keep-intermediate-files 不能与 --download-annotation-only 选项同时使用"
                    )
                )
            )
            exit(1)
        if not (args.download_for_archive or args.preview_video or args.generate_video):
            Stderr(
                RedText(
                    _(
                        "--no-keep-intermediate-files 必须和 --download-for-archive 或 --preview-video 或 --generate-video 选项使用"
                    )
                )
            )
            exit(1)

    if args.output is not None:
        if args.output_directory is not None:
            Stderr(RedText(_("--output 不能与 --output--directory 选项同时使用")))
            exit(1)
        if len(args.queue) > 1:
            Stderr(RedText(_("--output 只能处理一个文件")))
            exit(1)

    if args.output_directory is not None:
        if os.path.isdir(args.output_directory) is False:
            Stderr(RedText(_("转换后文件输出目录应该指定一个文件夹")))
            exit(1)

    if args.preview_video or args.generate_video:
        args.download_for_archive = True
        args.embrace_libass = True

    if args.embrace_libass and (
        args.transform_resolution_x == 100 or args.transform_resolution_y == 100
    ):
        Stderr(
            YellowText(
                _(
                    "如果您的视频不是 16:9, 请使用 --transform-resolution-x --transform-resolution-y, 以确保效果"
                )
            )
        )

    if args.download_annotation_only:
        args.download_for_archive = True

    if args.download_for_archive:
        # 省的网不好不知道
        def CheckNetwork():
            if CheckUrl() is False:
                Stderr(YellowText(_("您好像无法访问 Google 🤔")))

        _thread.start_new_thread(CheckNetwork, ())

    for Task in args.queue:
        videoId = Task
        annotationFile = Task
        if args.download_for_archive:
            if re.match(r"[a-zA-Z0-9_-]{11}", videoId) is None:
                Stderr(RedText(_("{} 不是一个有效的视频 ID").format(videoId)))
                continue

            annotationFile = f"{videoId}.xml"
            if args.download_annotation_only and args.output:
                annotationFile = args.output
            if args.output_directory is not None:
                annotationFile = os.path.join(args.output_directory, annotationFile)

            skipDownload = False
            if args.no_overwrite_files and os.path.exists(annotationFile):
                if os.path.exists(annotationFile):
                    Stderr(YellowText(_("文件已存在, 跳过下载 ({})").format(videoId)))
                    skipDownload = True
            if not skipDownload:
                url = AnnotationsForArchive(videoId)
                Stderr(_("下载 {}").format(url))
                with urllib.request.urlopen(url) as r:
                    string = r.read().decode("utf-8")
                with open(annotationFile, "w", encoding="utf-8") as f:
                    f.write(string)

            if args.download_annotation_only:
                continue

        if os.path.isfile(annotationFile) is False:
            Stderr(RedText(_("{} 不是一个文件").format(annotationFile)))
            continue

        with open(annotationFile, "r", encoding="utf-8") as f:
            annotationsString = f.read()

        if annotationsString == "":
            Stderr(YellowText(_("{} 可能没有 Annotation").format(Task)))
            continue

        try:
            tree = defusedxml.ElementTree.parse(annotationFile)
        except:
            Stderr(RedText(_("{} 不是一个有效的 XML 文件").format(annotationFile)))
            if Flags.verbose:
                Stderr(traceback.format_exc())
            continue

        if tree.find("annotations") == None:
            Stderr(RedText(_("{} 不是 Annotation 文件").format(annotationFile)))
            continue

        if len(tree.find("annotations").findall("annotation")) == 0:
            Stderr(YellowText(_("{} 没有 Annotation").format(annotationFile)))

        subFile = annotationFile + ".ass"
        if args.output_directory is not None:
            fileName = os.path.basename(annotationFile)
            fileName = fileName + ".ass"
            subFile = os.path.join(args.output_directory, fileName)
        if args.output is not None:
            subFile = args.output

        # 这里是 __init__.py 开头那个流程图
        with open(annotationFile, "r", encoding="utf-8") as f:
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
            Stderr(YellowText(_("{} 没有注释被转换").format(annotationFile)))
        # Annotation 是无序的
        # 按时间重新排列字幕事件, 是为了人类可读
        events.sort(key=lambda event: event.Start)
        sub = Sub()
        sub.events.extend(events)
        sub.info["PlayResX"] = args.transform_resolution_x
        sub.info["PlayResY"] = args.transform_resolution_y
        sub.info["Title"] = annotationFile
        sub.styles["Default"].Fontname = args.font
        subString = sub.Dump()
        if args.output_to_stdout:
            subFile = ""
            print(subString, file=sys.stdout)
        if args.no_overwrite_files:
            if os.path.exists(subFile):
                Stderr(YellowText(_("文件已存在, 跳过输出 ({})").format(subFile)))
                subFile = ""
        if args.no_keep_intermediate_files:
            os.remove(annotationFile)
            Stderr(_("删除 {}").format(annotationFile))
        if subFile != "":
            with open(subFile, "w", encoding="utf-8") as f:
                f.write(subString)
            Stderr(_("保存于: {}").format(subFile))

        if args.preview_video:
            # 从 Invidious 获取视频流和音频流, 并塞给 mpv, FFmpeg
            video, audio = VideoForInvidious(videoId, args.invidious_instances)
            cmd = rf'mpv "{video}" --audio-file="{audio}" --sub-file="{subFile}"'
            if Flags.verbose:
                Stderr(cmd)
            exit_code = os.system(cmd)
            if Flags.verbose:
                if exit_code != 0:
                    Stderr(YellowText("exit with {}".format(exit_code)))
            if args.no_keep_intermediate_files:
                os.remove(subFile)
                Stderr(_("删除 {}").format(subFile))

        if args.generate_video:
            video, audio = VideoForInvidious(videoId, args.invidious_instances)
            cmd = rf'ffmpeg -i "{video}" -i "{audio}" -vf "ass={subFile}" {subFile}.mp4'
            if Flags.verbose:
                Stderr(cmd)
            exit_code = os.system(cmd)
            if Flags.verbose:
                if exit_code != 0:
                    Stderr(YellowText("exit with {}".format(exit_code)))
            if args.no_keep_intermediate_files:
                os.remove(subFile)
                Stderr(_("删除 {}").format(subFile))
