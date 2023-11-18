#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.request
from urllib.error import URLError

import pytest

from Annotations2Sub import cli
from Annotations2Sub.cli import run
from Annotations2Sub.utils import Stderr

basePath = os.path.dirname(__file__)
testCasePath = os.path.join(basePath, "testCase")
baselinePath = os.path.join(testCasePath, "Baseline")

baseline1VideoId = "29-q7YnyUmY"
baseline2VideoId = "e8kKeUuytqA"

baseline1File = os.path.join(baselinePath, "29-q7YnyUmY.xml.test")
baseline2File = os.path.join(baselinePath, "e8kKeUuytqA.xml.test")

emptyXML = os.path.join(testCasePath, "empty.xml.test")
emptyAnnotations = os.path.join(testCasePath, "emptyAnnotations.xml.test")
file1 = os.path.join(testCasePath, "file.ass.test")


def test_cli():
    """预期失败的命令"""
    test = f"""-ND {baseline1File}
{baseline1File} -O {file1}
{baseline1File} {baseline2File} -o 1.ass
{baseline1File} -O . -o 1.ass
{emptyXML}
{file1}
0
-d 0"""

    for line in test.splitlines():
        Stderr(line)
        argv = line.split(" ")
        code = run(argv)
        assert code == 1


def test_cli2():
    """预期成功的命令"""
    test = f"""{baseline1File} {baseline2File} -l -x 1920 -y 1080 -f Microsoft -V -O .
{baseline1File} -o 1.ass
{baseline1File} -o -
{baseline1File} -n
{emptyAnnotations}"""

    for line in test.splitlines():
        Stderr(line)
        argv = line.split(" ")
        code = run(argv)
        assert code == 0


def test_cli3():
    """网络相关"""
    test = f"""-g {baseline1VideoId} -O .
-D {baseline1VideoId} -o 1.xml
-g {baseline1VideoId} -i 2
-D {baseline1VideoId} -o -
-dNn {baseline1VideoId}
-pN {baseline1VideoId}
-gn {baseline1VideoId}
-pg {baseline1VideoId}
-D {baseline1VideoId}
-g {baseline1VideoId}"""

    instancesString = r'{"adaptiveFormats":[{"type":"video","bitrate":1,"url":"1"},{"type":"audio","bitrate":1,"url":"2"}]}'
    invidiousString = r'[["0",{"api":false}],["1"],["2"]]'
    with open(baseline1File, encoding="utf-8") as f:
        baseline1String = f.read()

    def mock(url: str):
        if (
            url
            == "https://archive.org/download/youtubeannotations_54/29.tar/29-/29-q7YnyUmY.xml"
        ):
            return baseline1String
        if url == "https://api.invidious.io/instances.json":
            return invidiousString
        if url == "https://1/api/v1/videos/29-q7YnyUmY":
            return ""
        if url == "https://2/api/v1/videos/29-q7YnyUmY":
            return instancesString

        raise Exception

    m = pytest.MonkeyPatch()
    m.setattr(cli, "GetUrl", mock)
    m.setattr(os, "system", lambda __: None)

    for line in test.splitlines():
        Stderr(line)
        argv = line.split(" ")
        code = run(argv)
        assert code == 0

    with pytest.raises(Exception):
        run(f"-g {baseline1VideoId} -i 1".split(" "))

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
