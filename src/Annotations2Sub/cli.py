# -*- coding: utf-8 -*-


import argparse
import os
import sys
import traceback
from typing import Optional
from xml.etree.ElementTree import ParseError

from Annotations2Sub import __version__ as version
from Annotations2Sub.Annotations import NotAnnotationsDocumentError
from Annotations2Sub.cli_utils import (
    AnnotationsStringIsEmptyError,
    AnnotationsXmlStringToSubtitlesString,
)
from Annotations2Sub.flags import Flags
from Annotations2Sub.i18n import _
from Annotations2Sub.utils import Err, Info, Stderr, Warn


def Run(args=None) -> int:
    """跑起来🐎🐎🐎"""

    exit_code = 0
    parser = argparse.ArgumentParser(description=_("转换 Youtube 注释"))
    parser.add_argument(
        "queue",
        nargs="+",
        type=str,
        metavar=_("文件"),
        help=_("多个需要转换的文件的文件路径"),
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
        "-n", "--no-overwrite-files", action="store_true", help=_("不覆盖文件")
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

    args = parser.parse_args(args)
    queue = list(map(str, args.queue))

    transform_resolution_x: int = args.transform_resolution_x
    transform_resolution_y: int = args.transform_resolution_y
    font: str = args.font
    enable_no_overwrite_files: bool = args.no_overwrite_files
    output: Optional[str] = args.output
    output_directory: Optional[str] = args.output_directory
    enable_verbose: bool = args.verbose

    output_to_stdout = False

    if enable_verbose:
        Flags.verbose = True

    if output != None:
        if output_directory != None:
            Err(_("--output 不能与 --output--directory 选项同时使用"))
            return 2
        if len(queue) > 1:
            Err(_("--output 只能处理一个文件"))
            return 2
        if args.output == "-":
            output_to_stdout = True

    if output_directory is not None:
        if os.path.isdir(output_directory) is False:
            Err(_("转换后文件输出目录应该指定一个文件夹"))
            return 2

    for Task in queue:
        annotations_file = Task

        if os.path.isfile(annotations_file) is False:
            Err(_('"{}" 不是一个文件').format(annotations_file))
            exit_code += 13
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
            subtitle_string = AnnotationsXmlStringToSubtitlesString(
                annotations_string,
                transform_resolution_x,
                transform_resolution_y,
                font,
                os.path.basename(annotations_file),
            )

        except NotAnnotationsDocumentError:
            Err(_('"{}" 不是 Annotations 文件').format(annotations_file))
            exit_code += 14
            continue
        except ParseError:
            Err(_('"{}" 不是一个有效的 XML 文件').format(annotations_file))
            Info(traceback.format_exc())
            exit_code += 15
            continue
        except AnnotationsStringIsEmptyError:
            Err(_('"{}" 是空文件').format(annotations_file))
            exit_code += 20
            continue

        is_no_save = False
        if output_to_stdout:
            is_no_save = True
            sys.stdout.write(subtitle_string)

        if enable_no_overwrite_files:
            if os.path.exists(subtitle_file):
                Warn(_("文件已存在, 跳过输出 ({})").format(subtitle_file))
                is_no_save = True

        if not is_no_save:
            with open(subtitle_file, "w", encoding="utf-8") as f:
                f.write(subtitle_string)
            Stderr(_('保存于 "{}"').format(subtitle_file))

    if exit_code > 21:
        Warn(_("处理过程中出现多个错误"))
        exit_code = 18

    return exit_code
