#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import _thread
import argparse
import json
import os
import re
import subprocess
import sys
import traceback
import urllib.request
import xml.etree.ElementTree
from http.client import IncompleteRead
from urllib.error import URLError
from xml.etree.ElementTree import ParseError

from Annotations2Sub import Convert, Parse, Sub, version
from Annotations2Sub.utils import (
    Err,
    Flags,
    GetAnnotationsUrl,
    GetUrl,
    Info,
    MakeSureStr,
    Stderr,
    Warn,
    YellowText,
    _,
)


def Dummy(*args, **kwargs):
    """用于 MonkeyPatch"""


def GetMedia(videoId: str, instanceDomain: str) -> tuple[str, str]:
    url = f"https://{instanceDomain}/api/v1/videos/{videoId}"
    Stderr(_("获取 {}").format(url))
    data = json.loads(GetUrl(url))
    videos = []
    audios = []
    for i in data.get("adaptiveFormats"):
        if re.match("video", i.get("type")) != None:
            videos.append(i)
        if re.match("audio", i.get("type")) != None:
            audios.append(i)
    videos.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
    audios.sort(key=lambda x: int(x.get("bitrate")), reverse=True)
    video = MakeSureStr(videos[0]["url"])
    audio = MakeSureStr(audios[0]["url"])
    if not video.startswith("http"):
        raise ValueError(_("没有 Video"))
    if not audio.startswith("http"):
        raise ValueError(_("没有 Audio"))
    return video, audio


def Run(argv=None) -> int:
    """跑起来🐎🐎🐎"""

    exit_code = 0
    parser = argparse.ArgumentParser(description=_("下载和转换 Youtube 注释"))
    parser.add_argument(
        "queue",
        nargs="+",
        type=str,
        metavar=_("文件 或 videoId"),
        help=_("多个需要转换的文件的文件路径或视频ID"),
    )
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
    # 应该使用非衬线字体, 但是 SSA 不能方便的指定字体家族
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
        "--download-annotations-only",
        action="store_true",
        help=_("仅下载注释"),
    )
    parser.add_argument(
        "-i",
        "--invidious-instances",
        type=str,
        metavar="invidious.domain",
        help=_("指定 invidious 实例(https://redirect.invidious.io/)"),
    )
    # 拼接参数运行 mpv
    parser.add_argument(
        "-p",
        "--preview-video",
        action="store_true",
        help=_("预览视频, 需要 mpv(https://mpv.io/)"),
    )
    parser.add_argument(
        "-g",
        "--generate-video",
        action="store_true",
        help=_("生成视频, 需要 FFmpeg(https://ffmpeg.org/)"),
    )
    parser.add_argument(
        "-n", "--no-overwrite-files", action="store_true", help=_("不覆盖文件")
    )
    parser.add_argument(
        "-N", "--no-keep-intermediate-files", action="store_true", help=_("不保留中间文件")
    )
    parser.add_argument(
        "-o", "--output", type=str, metavar=_("文件"), help=_('保存到此文件, 如果为 "-" 则输出到标准输出')
    )
    parser.add_argument(
        "-O",
        "--output-directory",
        type=str,
        metavar=_("目录"),
        help=_("指定转换后文件的输出目录"),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help=_("显示版本号"),
        version=_("Annotations2Sub v{version}").format(version=version),
    )
    parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        help=_("显示更多消息"),
    )

    args = parser.parse_args(argv)

    queue = args.queue

    transform_resolution_x = args.transform_resolution_x
    transform_resolution_y = args.transform_resolution_y
    font = args.font
    enable_download_for_archive = args.download_for_archive
    enable_download_annotations_only = args.download_annotations_only
    invidious_instances = args.invidious_instances
    enable_preview_video = args.preview_video
    enable_generate_video = args.generate_video
    enable_no_overwrite_files = args.no_overwrite_files
    enable_no_keep_intermediate_files = args.no_keep_intermediate_files
    output = args.output
    output_directory = args.output_directory
    enable_verbose = args.verbose

    output_to_stdout = False

    if enable_verbose:
        Flags.verbose = True

    if output != None:
        if output_directory != None:
            Err(_("--output 不能与 --output--directory 选项同时使用"))
            return 1
        if len(queue) > 1:
            Err(_("--output 只能处理一个文件"))
            return 1
        if args.output == "-":
            output_to_stdout = True

    if output_directory != None:
        if os.path.isdir(output_directory) is False:
            Err(_("转换后文件输出目录应该指定一个文件夹"))
            return 1

    if enable_preview_video or enable_generate_video:
        enable_download_for_archive = True
        if invidious_instances == None:
            invidious_instances = ""

    if enable_download_annotations_only:
        enable_download_for_archive = True

    if enable_download_for_archive:
        # 省的网不好不知道
        def CheckNetwork():
            try:
                with urllib.request.urlopen(url="http://google.com", timeout=3) as r:
                    r.read().decode("utf-8")
            except URLError:
                Warn(_("您好像无法访问 Google 🤔"))

        Dummy([CheckNetwork])
        _thread.start_new_thread(CheckNetwork, ())

    for Task in queue:
        video_id = MakeSureStr(Task)
        annotations_file = Task

        if enable_download_for_archive:
            if video_id.startswith("\\"):
                video_id = video_id.replace("\\", "", 1)

            if re.match(r"[a-zA-Z0-9_-]{11}", video_id) == None:
                Err(_("{} 不是一个有效的视频 ID").format(video_id))
                exit_code = 1
                continue

            annotations_file = f"{video_id}.xml"
            if enable_download_annotations_only and output:
                annotations_file = output

            if output_directory != None:
                annotations_file = os.path.join(output_directory, annotations_file)

            is_skip_download = False
            if enable_no_overwrite_files and os.path.exists(annotations_file):
                if os.path.exists(annotations_file):
                    Stderr(YellowText(_("文件已存在, 跳过下载 ({})").format(video_id)))
                    is_skip_download = True

            if not is_skip_download:
                annotations_url = GetAnnotationsUrl(video_id)
                Stderr(_("下载 {}").format(annotations_url))
                annotations_string = GetUrl(annotations_url)
                if annotations_string == "":
                    Warn(_("{} 可能没有 Annotations").format(video_id))
                    exit_code = 1
                    continue
                if output_to_stdout:
                    sys.stdout.write(annotations_string)
                else:
                    with open(annotations_file, "w", encoding="utf-8") as f:
                        f.write(annotations_string)

            if enable_download_annotations_only:
                continue

        if os.path.isfile(annotations_file) is False:
            Err(_("{} 不是一个文件").format(annotations_file))
            exit_code = 1
            continue

        subtitle_file = annotations_file + ".ass"
        if output_directory != None:
            file_name = os.path.basename(annotations_file)
            file_name = file_name + ".ass"
            subtitle_file = os.path.join(output_directory, file_name)

        if output != None:
            subtitle_file = output

        with open(annotations_file, "r", encoding="utf-8") as f:
            annotations_string = f.read()

        try:
            tree = xml.etree.ElementTree.fromstring(annotations_string)
        except ParseError:
            Err(_("{} 不是一个有效的 XML 文件").format(annotations_file))
            Info(traceback.format_exc())
            exit_code = 1
            continue

        try:
            annotations = Parse(tree)
        except ValueError:
            Err(_("{} 不是 Annotations 文件").format(annotations_file))
            exit_code = 1
            continue

        events = Convert(
            annotations,
            transform_resolution_x,
            transform_resolution_y,
        )
        if events == []:
            Warn(_("{} 没有注释被转换").format(annotations_file))
        # Annotations 是无序的
        # 按时间重新排列字幕事件, 是为了人类可读
        events.sort(key=lambda event: event.Start)

        subtitle = Sub()
        subtitle.comment += _("此脚本使用 Annotations2Sub 生成") + "\n"
        subtitle.comment += "https://github.com/USED255/Annotations2Sub"
        subtitle.info["Title"] = os.path.basename(annotations_file)
        subtitle.info["PlayResX"] = transform_resolution_x
        subtitle.info["PlayResY"] = transform_resolution_y
        subtitle.info["WrapStyle"] = "2"
        subtitle.styles["Default"].Fontname = font
        subtitle.events.extend(events)
        subtitle_string = subtitle.Dump()

        is_no_save = False
        if output_to_stdout:
            is_no_save = True
            sys.stdout.write(subtitle_string)

        if enable_no_overwrite_files:
            if os.path.exists(subtitle_file):
                Stderr(YellowText(_("文件已存在, 跳过输出 ({})").format(subtitle_file)))
                is_no_save = True

        if enable_no_keep_intermediate_files:
            Stderr(_("删除 {}").format(annotations_file))
            os.remove(annotations_file)

        if not is_no_save:
            with open(subtitle_file, "w", encoding="utf-8") as f:
                f.write(subtitle_string)
            Stderr(_("保存于: {}").format(subtitle_file))

        def function2():
            Err(_("无法获取视频"))
            Stderr(traceback.format_exc())
            nonlocal exit_code
            exit_code = 1

        video = audio = ""
        if enable_preview_video or enable_generate_video:
            if invidious_instances == "":
                instances = json.loads(
                    GetUrl("https://api.invidious.io/instances.json")
                )
                for instance in instances:
                    try:
                        if not instance[1]["api"]:
                            continue
                    except IndexError:
                        pass
                    domain = instance[0]

                    try:
                        video, audio = GetMedia(video_id, domain)
                    except (json.JSONDecodeError, URLError, IncompleteRead, ValueError):
                        continue

                if video == "" or audio == "":
                    function2()
                    continue
            else:
                try:
                    video, audio = GetMedia(video_id, invidious_instances)
                except (json.JSONDecodeError, URLError, ValueError):
                    function2()
                    continue

        def function1():
            Info(" ".join(commands))

            _exit_code = subprocess.run(commands).returncode
            if _exit_code != 0:
                Stderr(YellowText("exit with {}".format(_exit_code)))
                nonlocal exit_code
                exit_code = 1

            if enable_no_keep_intermediate_files:
                Stderr(_("删除 {}").format(subtitle_file))
                os.remove(subtitle_file)

        if enable_preview_video:
            commands = [
                "mpv",
                video,
                f"--audio-file={audio}",
                f"--sub-file={subtitle_file}",
            ]
            function1()

        if enable_generate_video:
            commands = [
                "ffmpeg",
                "-i",
                video,
                "-i",
                audio,
                "-vf",
                f"ass={subtitle_file}",
                f"{subtitle_file}.mp4",
            ]
            function1()

    return exit_code
