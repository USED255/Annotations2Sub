# -*- coding: utf-8 -*-

import os
import subprocess
import urllib.request
from urllib.error import URLError

import pytest

from Annotations2Sub import cli, utils2
from Annotations2Sub.cli import Run
from Annotations2Sub.utils import Stderr
from tests import baselinePath, testCasePath

baseline1_video_id = "29-q7YnyUmY"

baseline1_file = os.path.join(baselinePath, "29-q7YnyUmY.xml.test")
baseline2_file = os.path.join(baselinePath, "e8kKeUuytqA.xml.test")

empty_xml = os.path.join(testCasePath, "empty.xml.test")
empty_annotations = os.path.join(testCasePath, "emptyAnnotations.xml.test")
file_file = os.path.join(testCasePath, "file.ass.test")


def test_cli_failed():
    """预期失败的命令"""
    commands = f"""-ND {baseline1_file}
{baseline1_file} -O {file_file}
{baseline1_file} {baseline2_file} -o 1.ass
{baseline1_file} -O . -o 1.ass
{empty_xml}
{file_file}
0
-d 0"""

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = Run(argv)
        assert code == 1


def test_cli_success():
    """预期成功的命令"""
    commands = f"""{baseline1_file} {baseline2_file} -x 1920 -y 1080 -f Microsoft -V -O .
{baseline1_file} -o annotations.ass
{baseline1_file} -o -
{baseline1_file} -n
{empty_annotations}"""

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = Run(argv)
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

    def GetUrlMock(url: str):
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

    def subprocessMock(*args, **kwargs):
        class a:
            def __init__(self):
                self.returncode = 1

        return a()

    m = pytest.MonkeyPatch()
    m.setattr(cli, "GetUrl", GetUrlMock)
    m.setattr(utils2, "GetUrl", GetUrlMock)
    m.setattr(subprocess, "run", subprocessMock)

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = Run(argv)
        assert code == 1

    with pytest.raises(pytest.fail.Exception):
        GetUrlMock("")

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

    def GetUrlMock(url: str):
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

    def subprocessMock(*args, **kwargs):
        class a:
            def __init__(self):
                self.returncode = 0

        return a()

    m = pytest.MonkeyPatch()
    m.setattr(cli, "GetUrl", GetUrlMock)
    m.setattr(utils2, "GetUrl", GetUrlMock)
    m.setattr(subprocess, "run", subprocessMock)

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = Run(argv)
        assert code == 0

    with pytest.raises(pytest.fail.Exception):
        GetUrlMock("")

    m.undo()


def test_CheckNetwork():
    def f(x):
        for i in x:
            if i.__name__ == "CheckNetwork":
                i()

    def urlopenMock(url, **kwargs):
        class mock:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                return b""

        return mock()

    def urlopenURLErrorMock(*args, **kwargs):
        raise URLError("")

    def GetUrlMock(url: str):
        if (
            url
            == "https://archive.org/download/youtubeannotations_53/12.tar/123/12345678911.xml"
        ):
            return ""
        pytest.fail()

    m = pytest.MonkeyPatch()
    m.setattr(cli, "Dummy", f)
    m.setattr(cli, "GetUrl", GetUrlMock)

    m.setattr(urllib.request, "urlopen", urlopenMock)
    Run("-d 12345678911".split(" "))

    m.setattr(urllib.request, "urlopen", urlopenURLErrorMock)
    Run("-d 12345678911".split(" "))

    with pytest.raises(pytest.fail.Exception):
        GetUrlMock("")

    m.undo()
