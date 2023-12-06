#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import _thread
import argparse
import json
import os
import re
import sys
import traceback
import urllib.request
from urllib.error import URLError
from xml.etree.ElementTree import ParseError

# 我觉得在输入确定的环境下用不着这玩意
# 不过打包到了 PyPI 也不用像以前那样忌惮第三方库了
# 不用白不用
import defusedxml.ElementTree  # type: ignore

from Annotations2Sub import version
from Annotations2Sub.Annotation import Parse
from Annotations2Sub.Convert import Convert
from Annotations2Sub.Sub import Sub
from Annotations2Sub.utils import (
    Flags,
    MakeSureStr,
    Stderr,
    YellowText,
    _,
    GetUrl,
    Err,
    Warn,
)


def Dummy(*args, **kwargs):
    """用于 MonkeyPatch"""
    pass


def run(argv=None):
    """跑起来🐎🐎🐎"""

    def CheckUrl(url: str = "https://google.com/", timeout: float = 3.0) -> bool:
        try:
            urllib.request.urlopen(url=url, timeout=timeout)
        except URLError:
            return False
        return True

    def GetAnnotationsUrl(videoId: str) -> str:
        # 移植自 https://github.com/omarroth/invidious/blob/ea0d52c0b85c0207c1766e1dc5d1bd0778485cad/src/invidious.cr#L2835
        # 向 https://archive.org/details/youtubeannotations 致敬
        # 如果你对你的数据在意, 就不要把它们托付给他人
        # Rain Shimotsuki 不仅是个打歌词的, 他更是一位创作者
        # 自己作品消失, 我相信没人愿意看到
        """返回注释在互联网档案馆的网址"""
        ARCHIVE_URL = "https://archive.org"
        CHARS_SAFE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

        if re.match(r"[a-zA-Z0-9_-]{11}", videoId) is None:
            raise ValueError("Invalid videoId")

        index = CHARS_SAFE.index(videoId[0]).__str__().rjust(2, "0")

        # IA doesn't handle leading hyphens,
        # so we use https://archive.org/details/youtubeannotations_64
        if index == "62":
            index = "64"
            videoId.replace("^-", "A")

        file = f"{videoId[0:3]}/{videoId}.xml"

        return f"{ARCHIVE_URL}/download/youtubeannotations_{index}/{videoId[0:2]}.tar/{file}"

    def AutoGetMedia(videoId: str) -> tuple:
        """返回视频流和音频流网址"""
        instances = []
        instances = json.loads(GetUrl("https://api.invidious.io/instances.json"))
        for instance in instances:
            try:
                if not instance[1]["api"]:  # type: ignore
                    continue
            except IndexError:
                pass
            domain = instance[0]
            url = f"https://{domain}/api/v1/videos/{videoId}"
            Stderr(_("获取 {}").format(url))
            try:
                data = json.loads(GetUrl(url))
            except (json.JSONDecodeError, URLError):
                continue

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
            return video, audio

        raise Exception

    def GetMedia(videoId: str, instanceDomain: str) -> tuple:
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
        return video, audio

    Dummy([CheckUrl, GetAnnotationsUrl, AutoGetMedia])  # type: ignore

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
        "-l",
        "--embrace-libass",
        action="store_true",
        help=_("拥抱 libass 的怪癖和特性, 不指定此选项则会适配 xy-vsfilter"),
    )

    # 虽然把分辨率置为 100, 100 字幕滤镜也能正常定位, 但是正确的分辨率会让字幕滤更高兴
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
    # 拼接参数执行 mpv
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
        "-i",
        "--invidious-instances",
        type=str,
        metavar="invidious.domain",
        help=_("指定 invidious 实例(https://redirect.invidious.io/)"),
    )

    parser.add_argument(
        "-n", "--no-overwrite-files", action="store_true", help=_("不覆盖文件")
    )

    # 指从 Internet Archive 下载的注释文件
    parser.add_argument(
        "-N", "--no-keep-intermediate-files", action="store_true", help=_("不保留中间文件")
    )

    parser.add_argument(
        "-O",
        "--output-directory",
        type=str,
        metavar=_("目录"),
        help=_("指定转换后文件的输出目录"),
    )
    parser.add_argument(
        "-o", "--output", type=str, metavar=_("文件"), help=_('保存到此文件, 如果为 "-" 则输出到标准输出')
    )
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

    args = parser.parse_args(argv)

    queue = args.queue

    enable_embrace_libass = args.embrace_libass
    transform_resolution_x = args.transform_resolution_x
    transform_resolution_y = args.transform_resolution_y
    font = args.font
    enable_download_for_archive = args.download_for_archive
    enable_download_annotation_only = args.download_annotation_only
    enable_preview_video = args.preview_video
    enable_generate_video = args.generate_video
    invidious_instances = args.invidious_instances
    enable_no_overwrite_files = args.no_overwrite_files
    enable_no_keep_intermediate_files = args.no_keep_intermediate_files
    output_directory = args.output_directory
    output = args.output
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
        enable_embrace_libass = True
        if invidious_instances == None:
            invidious_instances = ""

    if enable_embrace_libass and (
        transform_resolution_x == 100 or transform_resolution_y == 100
    ):
        Warn(
            _(
                "如果您的视频不是 16:9, 请使用 --transform-resolution-x --transform-resolution-y, 以确保效果"
            )
        )

    if enable_download_annotation_only:
        enable_download_for_archive = True

    if enable_download_for_archive:
        # 省的网不好不知道
        def CheckNetwork():
            if CheckUrl() is False:
                Warn(_("您好像无法访问 Google 🤔"))

        _thread.start_new_thread(CheckNetwork, ())

    for Task in queue:
        video_id = MakeSureStr(Task)
        annotation_file = Task

        if enable_download_for_archive:
            if video_id.startswith("\\"):
                video_id = video_id.replace("\\", "", 1)
            if re.match(r"[a-zA-Z0-9_-]{11}", video_id) is None:
                Err(_("{} 不是一个有效的视频 ID").format(video_id))
                exit_code = 1
                continue

            annotation_file = f"{video_id}.xml"
            if enable_download_annotation_only and output:
                annotation_file = output
            if output_directory != None:
                annotation_file = os.path.join(output_directory, annotation_file)

            is_skip_download = False
            if enable_no_overwrite_files and os.path.exists(annotation_file):
                if os.path.exists(annotation_file):
                    Stderr(YellowText(_("文件已存在, 跳过下载 ({})").format(video_id)))
                    is_skip_download = True
            if not is_skip_download:
                url = GetAnnotationsUrl(video_id)
                Stderr(_("下载 {}").format(url))
                string = GetUrl(url)
                if output_to_stdout:
                    print(string, file=sys.stdout)
                    continue
                with open(annotation_file, "w", encoding="utf-8") as f:
                    f.write(string)

            if enable_download_annotation_only:
                continue

        if os.path.isfile(annotation_file) is False:
            Err(_("{} 不是一个文件").format(annotation_file))
            exit_code = 1
            continue

        with open(annotation_file, "r", encoding="utf-8") as f:
            annotations_string = f.read()

        if annotations_string == "":
            Warn(_("{} 可能没有 Annotation").format(video_id))
            exit_code = 1
            continue

        try:
            tree = defusedxml.ElementTree.parse(annotation_file)
        except ParseError:
            Err(_("{} 不是一个有效的 XML 文件").format(annotation_file))
            if Flags.verbose:
                Stderr(traceback.format_exc())
            exit_code = 1
            continue

        if tree.find("annotations") == None:
            Err(_("{} 不是 Annotation 文件").format(annotation_file))
            exit_code = 1
            continue

        if len(tree.find("annotations").findall("annotation")) == 0:
            Warn(_("{} 没有 Annotation").format(annotation_file))

        subtitle_file = annotation_file + ".ass"
        if output_directory != None:
            file_name = os.path.basename(annotation_file)
            file_name = file_name + ".ass"
            subtitle_file = os.path.join(output_directory, file_name)
        if output != None:
            subtitle_file = output

        # 这里是 __init__.py 开头那个流程图
        with open(annotation_file, "r", encoding="utf-8") as f:
            string = f.read()
        tree = defusedxml.ElementTree.fromstring(string)
        annotations = Parse(tree)
        events = Convert(
            annotations,
            enable_embrace_libass,
            transform_resolution_x,
            transform_resolution_y,
        )
        if events == []:
            Warn(_("{} 没有注释被转换").format(annotation_file))
        # Annotation 是无序的
        # 按时间重新排列字幕事件, 是为了人类可读
        events.sort(key=lambda event: event.Start)
        subtitle = Sub()
        subtitle.events.extend(events)
        subtitle.comment += _("此脚本使用 Annotations2Sub 生成") + "\n"
        subtitle.comment += "https://github.com/USED255/Annotations2Sub"
        subtitle.info["PlayResX"] = transform_resolution_x  # type: ignore
        subtitle.info["PlayResY"] = transform_resolution_y  # type: ignore
        subtitle.info["Title"] = os.path.basename(annotation_file)
        subtitle.styles["Default"].Fontname = font
        subtitle_string = subtitle.Dump()
        is_no_save = False
        if output_to_stdout:
            is_no_save = True
            print(subtitle_string, file=sys.stdout)
        if enable_no_overwrite_files:
            if os.path.exists(subtitle_file):
                Stderr(YellowText(_("文件已存在, 跳过输出 ({})").format(subtitle_file)))
                is_no_save = True
        if enable_no_keep_intermediate_files:
            os.remove(annotation_file)
            Stderr(_("删除 {}").format(annotation_file))
        if not is_no_save:
            with open(subtitle_file, "w", encoding="utf-8") as f:
                f.write(subtitle_string)
            Stderr(_("保存于: {}").format(subtitle_file))

        def function1():
            if Flags.verbose:
                Stderr(cmd)
            exit_code = os.system(cmd)
            if Flags.verbose:
                if exit_code != 0:
                    Stderr(YellowText("exit with {}".format(exit_code)))
            if enable_no_keep_intermediate_files:
                os.remove(subtitle_file)
                Stderr(_("删除 {}").format(subtitle_file))

        video = audio = ""
        if enable_preview_video or enable_generate_video:
            if invidious_instances == "":
                video, audio = AutoGetMedia(video_id)
            elif invidious_instances != "":
                try:
                    video, audio = GetMedia(video_id, invidious_instances)
                except json.JSONDecodeError:
                    Err(_("无法获取视频"))
                    Stderr(traceback.format_exc())
                    exit_code = 1
                    continue
            else:
                raise Exception

        if enable_preview_video:
            cmd = rf'mpv "{video}" --audio-file="{audio}" --sub-file="{subtitle_file}"'
            function1()

        if enable_generate_video:
            cmd = rf'ffmpeg -i "{video}" -i "{audio}" -vf "ass={subtitle_file}" {subtitle_file}.mp4'
            function1()

    return exit_code
