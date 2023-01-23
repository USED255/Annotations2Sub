#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.request
import pytest

from Annotations2Sub import cli
from Annotations2Sub.cli import run

path = os.path.dirname(__file__)
file1 = os.path.join(path, "Baseline", "29-q7YnyUmY.xml.test")
file2 = os.path.join(path, "Baseline", "e8kKeUuytqA.xml.test")
file3 = os.path.join(path, "test", "1.xml.test")
file4 = os.path.join(path, "test", "2.xml.test")
file5 = os.path.join(path, "test", "1.ass.test")


def test_cli():
    test = f"""-s {file1} -o {file5}
-s {file1} -n
-s {file1} -O {file5}
-s {file1} -D
-s {file1} -p
-s {file1} -g
-N {file1}
-N -D {file1}
{file1} -o {file5}
0
-d 0
{file3}
{file5}
{file1} {file2} -O 1.ass
{file1} -o . -O 1.ass"""
    for line in test.splitlines():
        argv = line.split(" ")
        code = run(argv)
        assert code == 1


def test_cli2():
    test = f"""{file1} {file2} -l -x 1920 -y 1080 -f Microsoft -V -o .
{file1} -l
{file1} -O 1.ass
{file1} -s
{file4}
{file1} -n
"""
    for line in test.splitlines():
        argv = line.split(" ")
        code = run(argv)
        assert code == 0


def test_cli3():
    m = pytest.MonkeyPatch()
    m.setattr(cli, "urllibWapper", lambda x: "")

    code = run(["-d", "29-q7YnyUmY"])
    assert code == 1


def test_cli4():
    def b(*args, **kwargs):
        raise Exception

    m = pytest.MonkeyPatch()
    m.setattr(urllib.request, "urlopen", b)
