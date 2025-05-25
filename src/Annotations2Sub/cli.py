# -*- coding: utf-8 -*-


import _thread
import argparse
# import json # No longer used directly
import os
import re
import subprocess
import sys
import traceback
import urllib.request # Still used by CheckNetwork, though it imports locally
# from http.client import IncompleteRead # No longer used directly
from typing import List, Optional
# from urllib.error import URLError # No longer used directly, CheckNetwork imports it locally
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
from Annotations2Sub.utils import Err, GetUrl, Info, Stderr, Warn, YellowText # GetUrl is still used for archive.org


def Dummy(*args, **kwargs):
    """用于 MonkeyPatch"""


def Run(argv=None):  # -> Literal[1, 0]:
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
    # parser.add_argument(
    #     "-i",
    #     "--invidious-instances",
    #     type=str,
    #     metavar="invidious.domain",
    #     help=_("指定 invidious 实例(https://redirect.invidious.io/)"),
    # ) # Removed
    # 拼接参数运行 mpv
    parser.add_argument(
        "-p",
        "--preview-video",
        action="store_true",
        help=_("预览视频, 需要 mpv(https://mpv.io/) 和 yt-dlp (请确保其在 PATH 中)"),
    )
    parser.add_argument(
        "-g",
        "--generate-video",
        action="store_true",
        help=_("生成视频, 需要 FFmpeg(https://ffmpeg.org/) 和 yt-dlp (请确保其在 PATH 中)"),
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
    # invidious_instances: Optional[str] = args.invidious_instances # Removed
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
        # if invidious_instances == None: # Removed
        #     invidious_instances = "" # Removed

    if enable_download_annotations_only:
        enable_download_for_archive = True

    if enable_download_for_archive:
        # 省的网不好不知道
        def CheckNetwork():
            # Local imports are fine as per previous diff, but ensure top-level are cleaned
            import urllib.request 
            from urllib.error import URLError 
            try:
                with urllib.request.urlopen(url="http://google.com", timeout=3) as r:
                    r.read().decode("utf-8")
            except (URLError, TimeoutError): # TimeoutError is built-in
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
            try:
                # Call GetMedia with None for instanceDomain, as it's handled by yt-dlp now.
                # The second argument to GetMedia is instanceDomain, which is deprecated.
                video, audio = GetMedia(video_id, None)
            except ValueError as e:
                Err(_("获取媒体失败 (yt-dlp): {}").format(e))
                if Flags.verbose:
                    Stderr(traceback.format_exc())
                exit_code = 1
                continue # Skip to next task in queue
            # Ensure video and audio are not empty if GetMedia succeeded without specific URLs
            # This check might be redundant if GetMedia guarantees non-empty strings or raises ValueError
            if not video or not audio:
                Err(_("获取媒体失败 (yt-dlp): 未找到有效的视频或音频 URL。"))
                exit_code = 1
                continue


        def run(commands: List[str]):
            # Ensure video and audio are available before running commands that use them
            if not video or not audio:
                # This state should ideally be caught above, but as a safeguard:
                Err(_("无法执行预览/生成，因为视频/音频 URL 未获取。"))
                nonlocal exit_code # ensure we can modify the outer scope's exit_code
                exit_code = 1
                return # Do not proceed with run

            Info(" ".join(commands))

            _exit_code = subprocess.run(commands).returncode
            if _exit_code != 0:
                Stderr(YellowText('exit with "{}"'.format(_exit_code)))
                nonlocal exit_code
                exit_code = 1

            if enable_no_keep_intermediate_files:
                # Only remove subtitle file if it exists
                if os.path.exists(subtitle_file):
                    Stderr(_('删除 "{}"').format(subtitle_file))
                    os.remove(subtitle_file)

        if enable_preview_video:
            if video and audio: # Proceed only if video and audio URLs are available
                commands = [
                    "mpv",
                    video,
                    f"--audio-file={audio}",
                    f"--sub-file={subtitle_file}",
                ]
                run(commands)
            else:
                # Error already printed, exit_code set, and loop continued by the GetMedia error handling.
                # This path should ideally not be reached if GetMedia error handling is robust.
                pass


        if enable_generate_video:
            if video and audio: # Proceed only if video and audio URLs are available
                video_output_filename = f"{subtitle_file}.mp4"
                if output_directory and not output:
                     base_name = os.path.basename(subtitle_file)
                     video_output_filename = os.path.join(output_directory, f"{base_name}.mp4")
                elif output and output != "-":
                    video_output_filename = f"{output}.mp4"
                elif output == "-":
                    Err(_("使用 stdout 进行字幕输出时不支持视频生成。请指定输出文件。"))
                    nonlocal exit_code
                    exit_code = 1
                    # We should not call run(commands) here
                else: # Not stdout, proceed with determined filename
                    commands = [
                        "ffmpeg",
                        "-i",
                        video,
                        "-i",
                        audio,
                        "-vf",
                        f"ass={subtitle_file}",
                        video_output_filename,
                    ]
                    run(commands)
                    if not enable_no_keep_intermediate_files and not is_no_save :
                        Stderr(_('视频保存于: "{}"').format(video_output_filename))
            else:
                # Error already printed, exit_code set, and loop continued by the GetMedia error handling.
                pass

    return exit_code
