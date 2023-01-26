#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.request

import pytest

from Annotations2Sub import cli
from Annotations2Sub.cli import run
from Annotations2Sub.utils import Stderr

basePath = os.path.dirname(__file__)
Baseline1 = "29-q7YnyUmY"
Baseline2 = "e8kKeUuytqA"
baseline1File = os.path.join(basePath, "Baseline", "29-q7YnyUmY.xml.test")
baseline2File = os.path.join(basePath, "Baseline", "e8kKeUuytqA.xml.test")
emptyXML = os.path.join(basePath, "test", "1.xml.test")
emptyAnnotations = os.path.join(basePath, "test", "2.xml.test")
ssa1 = os.path.join(basePath, "test", "1.ass.test")


def test_cli():
    """预期失败的命令"""
    test = f"""-s {baseline1File} -o {ssa1}
-s {baseline1File} -O {ssa1}
-sD {baseline1File}
-sp {baseline1File}
-sg {baseline1File}
-ND {baseline1File}
{baseline1File} -o {ssa1}
{baseline1File} {baseline2File} -O 1.ass
{baseline1File} -o . -O 1.ass
{emptyXML}
{ssa1}
0
-d 0"""

    for line in test.splitlines():
        Stderr(line)
        argv = line.split(" ")
        code = run(argv)
        assert code == 1


def test_cli2():
    """预期成功的命令"""
    test = f"""{baseline1File} {baseline2File} -l -x 1920 -y 1080 -f Microsoft -V -o .
{baseline1File} -O 1.ass
{baseline1File} -s
{baseline1File} -n
{emptyAnnotations}"""

    for line in test.splitlines():
        Stderr(line)
        argv = line.split(" ")
        code = run(argv)
        assert code == 0


def test_cli3():
    """网络相关"""
    test = f"""-g {Baseline1} -o .
-D {Baseline1} -O 1.xml
-g {Baseline1} -i 2
-D {Baseline1} -s
-dNn {Baseline1}
-pN {Baseline1}
-gn {Baseline1}
-pg {Baseline1}
-D {Baseline1}
-g {Baseline1}"""
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
    m.setattr(cli, "urllibWapper", mock)
    m.setattr(os, "system", lambda __: None)

    for line in test.splitlines():
        Stderr(line)
        argv = line.split(" ")
        code = run(argv)
        assert code == 0

    with pytest.raises(Exception):
        run(f"-g {Baseline1} -i 1".split(" "))

    with pytest.raises(Exception):
        mock("")

    m.undo()


def test_cli4():
    m = pytest.MonkeyPatch()
    m.setattr(cli, "urllibWapper", lambda x: "")
    assert run("""-d \\-9-q7YnyUmY""".split(" ")) == 1


def test_cli5():
    def f1(x):
        for i in x:
            if i.__name__ == "CheckUrl":
                i()

    def f2(*args, **kwargs):
        return

    def f3(*args, **kwargs):
        raise Exception

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
