#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
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


def test_cli():
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


def test_cli2():
    """预期成功的命令"""
    commands = f"""{baseline1_file} {baseline2_file} -l -x 1920 -y 1080 -f Microsoft -V -O .
{baseline1_file} -o 1.ass
{baseline1_file} -o -
{baseline1_file} -n
{empty_annotations}"""

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = run(argv)
        assert code == 0


def test_cli3():
    """网络相关"""
    commands = f"""-g {baseline1_video_id} -O .
-D {baseline1_video_id} -o 1.xml
-g {baseline1_video_id} -i 2
-D {baseline1_video_id} -o -
-dNn {baseline1_video_id}
-pN {baseline1_video_id}
-gn {baseline1_video_id}
-pg {baseline1_video_id}
-D {baseline1_video_id}
-g {baseline1_video_id}"""

    instances_string = r'{"adaptiveFormats":[{"type":"video","bitrate":1,"url":"1"},{"type":"audio","bitrate":1,"url":"2"}]}'
    invidious_string = r'[["0",{"api":false}],["1"],["2"]]'
    with open(baseline1_file, encoding="utf-8") as f:
        baseline1_string = f.read()

    def mock(url: str):
        if (
            url
            == "https://archive.org/download/youtubeannotations_54/29.tar/29-/29-q7YnyUmY.xml"
        ):
            return baseline1_string
        if url == "https://api.invidious.io/instances.json":
            return invidious_string
        if url == "https://1/api/v1/videos/29-q7YnyUmY":
            return ""
        if url == "https://2/api/v1/videos/29-q7YnyUmY":
            return instances_string

        raise Exception

    m = pytest.MonkeyPatch()
    m.setattr(cli, "GetUrl", mock)
    m.setattr(os, "system", lambda __: None)

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = run(argv)
        assert code == 0

    with pytest.raises(Exception):
        run(f"-g {baseline1_video_id} -i 1".split(" "))

    with pytest.raises(Exception):
        mock("")

    m.undo()


def test_cli4():
    m = pytest.MonkeyPatch()
    m.setattr(cli, "GetUrl", lambda x: "")
    assert run("""-d \\-9-q7YnyUmY""".split(" ")) == 1


def test_cli5():
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


def test_cli6():
    def f(x):
        for i in x:
            if i.__name__ == "AnnotationsFromArchive":
                i("")

    m = pytest.MonkeyPatch()
    m.setattr(cli, "Dummy", f)
    with pytest.raises(ValueError):
        run()

    m.undo()
