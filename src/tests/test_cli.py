#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import urllib.request
from urllib.error import URLError

import pytest

from Annotations2Sub import cli
from Annotations2Sub.cli import run
from Annotations2Sub.utils import Stderr

base_path = os.path.dirname(__file__)
test_case_path = os.path.join(base_path, "testCase")
baseline_path = os.path.join(test_case_path, "Baseline")

baseline1_video_id = "29-q7YnyUmY"
baseline2_video_id = "e8kKeUuytqA"

baseline1_file = os.path.join(baseline_path, "29-q7YnyUmY.xml.test")
baseline2_file = os.path.join(baseline_path, "e8kKeUuytqA.xml.test")

empty_xml = os.path.join(test_case_path, "empty.xml.test")
empty_annotations = os.path.join(test_case_path, "emptyAnnotations.xml.test")
file1 = os.path.join(test_case_path, "file.ass.test")


def test_cli_failed():
    """预期失败的命令"""
    commands = f"""-ND {baseline1_file}
{baseline1_file} -O {file1}
{baseline1_file} {baseline2_file} -o 1.ass
{baseline1_file} -O . -o 1.ass
{empty_xml}
{file1}
0
-d 0"""

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = run(argv)
        assert code == 1


def test_cli_success():
    """预期成功的命令"""
    commands = f"""{baseline1_file} {baseline2_file} -l -x 1920 -y 1080 -f Microsoft -V -O .
{baseline1_file} -o annotations.ass
{baseline1_file} -o -
{baseline1_file} -n
{empty_annotations}"""

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = run(argv)
        assert code == 0


def test_cli_network_failed():
    """网络相关"""
    commands = f"""-g {baseline1_video_id} -i bad.instance
-g {baseline1_video_id}
-g {baseline1_video_id} -i malicious.instance
-g {baseline1_video_id} -i malicious2.instance
-g {baseline1_video_id} -i malicious3.instance
-d 12345678911"""

    with open(baseline1_file, encoding="utf-8") as f:
        baseline1_string = f.read()

    def mock(url: str):
        if (
            url
            == "https://archive.org/download/youtubeannotations_53/12.tar/123/12345678911.xml"
        ):
            return ""
        if (
            url
            == "https://archive.org/download/youtubeannotations_54/29.tar/29-/29-q7YnyUmY.xml"
        ):
            return baseline1_string
        if url == "https://api.invidious.io/instances.json":
            return r'[["malicious.instance"],["malicious2.instance"]]'
        if url == "https://bad.instance/api/v1/videos/29-q7YnyUmY":
            return ""
        if url == "https://malicious.instance/api/v1/videos/29-q7YnyUmY":
            return r'{"adaptiveFormats":[{"type":"video","bitrate":1,"url":"file://c/"},{"type":"audio","bitrate":1,"url":"file://c/"}]}'
        if url == "https://malicious2.instance/api/v1/videos/29-q7YnyUmY":
            return r'{"adaptiveFormats":[{"type":"video","bitrate":1,"url":"http://c/"},{"type":"audio","bitrate":1,"url":"file://c/"}]}'
        if url == "https://malicious3.instance/api/v1/videos/29-q7YnyUmY":
            return r'{"adaptiveFormats":[{"type":"video","bitrate":1,"url":"http://c/"},{"type":"audio","bitrate":1,"url":"http://c/"}]}'

        pytest.fail()

    def f1(*args, **kwargs):
        class a:
            def __init__(self) -> None:
                self.returncode = 1

        return a()

    m = pytest.MonkeyPatch()
    m.setattr(cli, "GetUrl", mock)
    m.setattr(subprocess, "run", f1)

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = run(argv)
        assert code == 1

    with pytest.raises(pytest.fail.Exception):
        mock("")

    m.undo()


def test_cli_network_success():
    commands = f"""-g {baseline1_video_id} -O .
-D {baseline1_video_id} -o annotations.xml
-g {baseline1_video_id} -i good.instance
-D {baseline1_video_id} -o -
-dNn {baseline1_video_id}
-pN {baseline1_video_id}
-gn {baseline1_video_id}
-pg {baseline1_video_id}
-D {baseline1_video_id}
-g {baseline1_video_id}
-g -2345678911
-g \\12345678911
"""

    instances_string = r'{"adaptiveFormats":[{"type":"video","bitrate":1,"url":"https://1/video"},{"type":"audio","bitrate":1,"url":"https://1/audio"}]}'
    invidious_string = (
        r'[["noapi.instances",{"api":false}],["bad.instance"],["good.instance"]]'
    )
    with open(baseline1_file, encoding="utf-8") as f:
        baseline1_string = f.read()

    def mock(url: str):
        if (
            url
            == "https://archive.org/download/youtubeannotations_54/29.tar/29-/29-q7YnyUmY.xml"
        ):
            return baseline1_string
        if (
            url
            == "https://archive.org/download/youtubeannotations_53/12.tar/123/12345678911.xml"
        ):
            return baseline1_string
        if (
            url
            == "https://archive.org/download/youtubeannotations_64/-2.tar/-23/-2345678911.xml"
        ):
            return baseline1_string
        if url == "https://api.invidious.io/instances.json":
            return invidious_string
        if url == "https://good.instance/api/v1/videos/29-q7YnyUmY":
            return instances_string
        if url == "https://good.instance/api/v1/videos/12345678911":
            return instances_string
        if url == "https://good.instance/api/v1/videos/-2345678911":
            return instances_string
        if url == "https://bad.instance/api/v1/videos/29-q7YnyUmY":
            return ""
        if url == "https://bad.instance/api/v1/videos/12345678911":
            return ""
        if url == "https://bad.instance/api/v1/videos/-2345678911":
            return ""

        pytest.fail()

    def f1(*args, **kwargs):
        class a:
            def __init__(self) -> None:
                self.returncode = 0

        return a()

    m = pytest.MonkeyPatch()
    m.setattr(cli, "GetUrl", mock)
    m.setattr(subprocess, "run", f1)

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = run(argv)
        assert code == 0

    with pytest.raises(pytest.fail.Exception):
        mock("")

    m.undo()


def test_CheckUrl():
    def f1(x):
        for i in x:
            if i.__name__ == "CheckUrl":
                i()

    def f2(*args, **kwargs):
        return

    def f3(*args, **kwargs):
        raise URLError("")

    m = pytest.MonkeyPatch()
    m.setattr(cli, "Dummy", f1)

    m.setattr(urllib.request, "urlopen", f2)
    with pytest.raises(SystemExit):
        run([])

    m.setattr(urllib.request, "urlopen", f3)
    with pytest.raises(SystemExit):
        run([])

    m.undo()


def test_GetAnnotationsUrl_ValueError():
    def f(x):
        for i in x:
            if i.__name__ == "GetAnnotationsUrl":
                i("")

    m = pytest.MonkeyPatch()
    m.setattr(cli, "Dummy", f)

    with pytest.raises(ValueError):
        run()

    m.undo()
