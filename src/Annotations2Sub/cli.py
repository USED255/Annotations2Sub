# -*- coding: utf-8 -*-
"""Provides the command-line interface for the Annotations2Sub application.

This module is responsible for parsing command-line arguments, interpreting user
intent, and orchestrating the overall workflow. It handles tasks such as
fetching annotation files (from local paths or online sources like Internet Archive),
converting them to subtitle formats (primarily ASS), and managing options related
to output (filenames, directories, stdout), video resolution, font selection,
and integration with external tools like mpv for preview and FFmpeg for
video generation with hardcoded subtitles. It also controls verbosity and
error reporting to the user.
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
    """Main function for the Annotations2Sub command-line interface.

    This function orchestrates the entire process of the Annotations2Sub tool.
    It parses command-line arguments, processes a queue of video IDs or local
    XML file paths, downloads annotation files if requested, converts them to
    ASS subtitle format, and handles various output options. It can also
    initiate video preview with mpv or video generation with FFmpeg if specified.

    The function iterates through each item in the input queue (video IDs or file paths).
    For each item:
    1. If downloading is enabled:
        - It constructs the annotation URL (e.g., from Internet Archive).
        - Downloads the annotation XML content.
        - Saves it to a local file or outputs to stdout if requested.
        - If only download is requested, it skips further processing for this item.
    2. If not just downloading, or if a local file is provided:
        - Reads the annotation XML from the file.
        - Converts the XML content to an ASS subtitle string using
          `AnnotationsXmlStringToSub` from `cli_utils`. This involves parsing
          the XML, converting annotations to `Event` objects, and then to
          a `Sub` object.
        - Handles errors like invalid XML or non-annotation documents.
    3. Manages output:
        - Saves the resulting ASS subtitle string to a file (with a `.ass`
          extension, in a specified directory, or with a specified name)
          or prints to stdout.
        - Handles options like not overwriting existing files.
    4. If intermediate files are not to be kept, the original XML (if downloaded)
       and the generated ASS file (if used for video generation/preview) are deleted.
    5. If video preview (`-p`) or generation (`-g`) is enabled:
        - Fetches video and audio stream URLs using `GetMedia` from `cli_utils`,
          utilizing an Invidious instance.
        - Constructs and runs the appropriate command for `mpv` (preview) or
          `ffmpeg` (generation).

    Args:
        argv: A list of command-line arguments. If None, `sys.argv[1:]` is used.
              This allows the function to be called programmatically with specific
              arguments.

    Returns:
        An integer exit code: 0 for success, 1 for errors encountered during
        processing.
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
