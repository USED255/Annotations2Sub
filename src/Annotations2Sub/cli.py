# -*- coding: utf-8 -*-
"""为 Annotations2Sub 应用程序提供命令行界面。

此模块负责解析命令行参数、解释用户意图以及协调整个工作流程。
它处理的任务包括：获取注释文件（从本地路径或在线来源，如互联网档案馆）、
将其转换为字幕格式（主要是 ASS）、管理与输出相关的选项（文件名、目录、标准输出）、
视频分辨率、字体选择，以及与外部工具（如用于预览的 mpv 和用于生成硬编码字幕视频的 FFmpeg）的集成。
它还控制详细程度和向用户报告错误。
"""


import _thread
import argparse
import json
import os
import re
import subprocess
import sys
import traceback
import urllib.request
from http.client import IncompleteRead
from typing import List, Optional
from urllib.error import URLError
from xml.etree.ElementTree import ParseError

from Annotations2Sub import __version__ as version
from Annotations2Sub._flags import Flags
from Annotations2Sub.Annotations import NotAnnotationsDocumentError
from Annotations2Sub.cli_utils import (
    AnnotationsXmlStringToSub,
    GetAnnotationsUrl,
    GetMedia,
)
from Annotations2Sub.i18n import _
from Annotations2Sub.utils import Err, GetUrl, Info, Stderr, Warn, YellowText


def Dummy(*args, **kwargs):
    """用于 MonkeyPatch"""


def Run(argv: Optional[List[str]] = None) -> int:
    """Annotations2Sub 命令行界面的主函数。

    此函数协调 Annotations2Sub 工具的整个过程。
    它解析命令行参数，处理视频 ID 或本地 XML 文件路径队列，
    如果请求则下载注释文件，将其转换为 ASS 字幕格式，并处理各种输出选项。
    如果指定，它还可以使用 mpv 启动视频预览或使用 FFmpeg 生成视频。

    该函数遍历输入队列中的每个项目（视频 ID 或文件路径）。
    对于每个项目：
    1. 如果启用了下载：
        - 它会构建注释 URL（例如，从互联网档案馆）。
        - 下载注释 XML 内容。
        - 将其保存到本地文件，如果请求则输出到标准输出。
        - 如果仅请求下载，则跳过此项目的进一步处理。
    2. 如果不仅仅是下载，或者提供了本地文件：
        - 从文件读取注释 XML。
        - 使用 `cli_utils` 中的 `AnnotationsXmlStringToSub` 将 XML 内容转换为 ASS 字幕字符串。
          这包括解析 XML，将注释转换为 `Event` 对象，然后再转换为 `Sub` 对象。
        - 处理无效 XML 或非注释文档等错误。
    3. 管理输出：
        - 将生成的 ASS 字幕字符串保存到文件（扩展名为 `.ass`，
          在指定目录中，或使用指定名称）或打印到标准输出。
        - 处理不覆盖现有文件等选项。
    4. 如果不保留中间文件，则删除原始 XML（如果已下载）和生成的 ASS 文件
       （如果用于视频生成/预览）。
    5. 如果启用了视频预览 (`-p`) 或生成 (`-g`)：
        - 使用 `cli_utils` 中的 `GetMedia` 通过 Invidious 实例获取视频和音频流 URL。
        - 构建并运行适用于 `mpv` (预览) 或 `ffmpeg` (生成) 的相应命令。

    参数:
        argv: 命令行参数列表。如果为 None，则使用 `sys.argv[1:]`。
              这允许以编程方式使用特定参数调用该函数。

    返回:
        一个整数退出代码：0 表示成功，1 表示处理过程中遇到错误。
    """

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
        default=1000,
        type=int,
        metavar="1920",
        help=_("变换分辨率X"),
    )
    parser.add_argument(
        "-y",
        "--transform-resolution-y",
        default=1000,
        type=int,
        metavar="1080",
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
        "-N",
        "--no-keep-intermediate-files",
        action="store_true",
        help=_("不保留中间文件"),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar=_("文件"),
        help=_('保存到此文件, 如果为 "-" 则输出到标准输出'),
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
    queue = list(map(str, args.queue))

    transform_resolution_x: int = args.transform_resolution_x
    transform_resolution_y: int = args.transform_resolution_y
    font: str = args.font
    enable_download_for_archive: bool = args.download_for_archive
    enable_download_annotations_only: bool = args.download_annotations_only
    invidious_instances: Optional[str] = args.invidious_instances
    enable_preview_video: bool = args.preview_video
    enable_generate_video: bool = args.generate_video
    enable_no_overwrite_files: bool = args.no_overwrite_files
    enable_no_keep_intermediate_files: bool = args.no_keep_intermediate_files
    output: Optional[str] = args.output
    output_directory: Optional[str] = args.output_directory
    enable_verbose: bool = args.verbose

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

    if output_directory is not None:
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
            except (URLError, TimeoutError):
                Warn(_("您好像无法访问 Google 🤔"))

        _thread.start_new_thread(CheckNetwork, ())
        Dummy([CheckNetwork])

    for Task in queue:
        video_id = Task
        annotations_file = Task

        if enable_download_for_archive:
            if video_id.startswith("\\"):
                video_id = video_id.replace("\\", "", 1)

            if re.match(r"[a-zA-Z0-9_-]{11}", video_id) == None:
                Err(_('"{}" 不是一个有效的视频 ID').format(video_id))
                exit_code = 1
                continue

            annotations_file = f"{video_id}.xml"
            if enable_download_annotations_only and output:
                annotations_file = output

            if output_directory is not None:
                annotations_file = os.path.join(output_directory, annotations_file)

            is_skip_download = False
            if enable_no_overwrite_files and os.path.exists(annotations_file):
                if os.path.exists(annotations_file):
                    Stderr(YellowText(_("文件已存在, 跳过下载 ({})").format(video_id)))
                    is_skip_download = True

            if not is_skip_download:
                annotations_url = GetAnnotationsUrl(video_id)
                Stderr(_('下载 "{}"').format(annotations_url))
                annotations_string = GetUrl(annotations_url)
                if annotations_string == "":
                    Warn(_('"{}" 可能没有 Annotations').format(video_id))
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
            Err(_('"{}" 不是一个文件').format(annotations_file))
            exit_code = 1
            continue

        subtitle_file = annotations_file + ".ass"
        if output_directory is not None:
            file_name = os.path.basename(annotations_file)
            file_name = file_name + ".ass"
            subtitle_file = os.path.join(output_directory, file_name)

        if output is not None:
            subtitle_file = output

        with open(annotations_file, "r", encoding="utf-8") as f:
            annotations_string = f.read()

        try:
            subtitle_string = str(
                AnnotationsXmlStringToSub(
                    annotations_string,
                    transform_resolution_x,
                    transform_resolution_y,
                    font,
                    os.path.basename(annotations_file),
                )
            )
        except NotAnnotationsDocumentError:
            Err(_('"{}" 不是 Annotations 文件').format(annotations_file))
            exit_code = 1
            continue
        except ParseError:
            Err(_('"{}" 不是一个有效的 XML 文件').format(annotations_file))
            Info(traceback.format_exc())
            exit_code = 1
            continue

        is_no_save = False
        if output_to_stdout:
            is_no_save = True
            sys.stdout.write(subtitle_string)

        if enable_no_overwrite_files:
            if os.path.exists(subtitle_file):
                Stderr(YellowText(_("文件已存在, 跳过输出 ({})").format(subtitle_file)))
                is_no_save = True

        if enable_no_keep_intermediate_files:
            Stderr(_('删除 "{}"').format(annotations_file))
            os.remove(annotations_file)

        if not is_no_save:
            with open(subtitle_file, "w", encoding="utf-8") as f:
                f.write(subtitle_string)
            Stderr(_('保存于: "{}"').format(subtitle_file))

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
                    Err(_("无法获取视频"))
                    exit_code = 1
                    continue
            else:
                try:
                    video, audio = GetMedia(video_id, str(invidious_instances))
                except (json.JSONDecodeError, URLError, ValueError):
                    Err(_("无法获取视频"))
                    Stderr(traceback.format_exc())
                    exit_code = 1
                    continue

        def run(commands: List[str]):
            Info(" ".join(commands))

            _exit_code = subprocess.run(commands).returncode
            if _exit_code != 0:
                Stderr(YellowText('exit with "{}"'.format(_exit_code)))
                nonlocal exit_code
                exit_code = 1

            if enable_no_keep_intermediate_files:
                Stderr(_('删除 "{}"').format(subtitle_file))
                os.remove(subtitle_file)

        if enable_preview_video:
            commands = [
                "mpv",
                video,
                f"--audio-file={audio}",
                f"--sub-file={subtitle_file}",
            ]
            run(commands)

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
            run(commands)

    return exit_code
