#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from Annotations2Sub.cli import run

path = os.path.dirname(__file__)
path = os.path.join(path, "Baseline")
file1 = os.path.join(path, "29-q7YnyUmY.xml.test")
file2 = os.path.join(path, "e8kKeUuytqA.xml.test")


def test_cli():
    test = f"""-s {file1} -o 1.ass
-s {file1} -n
-s {file1} -O 1.ass
-s {file1} -D
-s {file1} -p
-s {file1} -g
-N {file1}
-N -D {file1}
{file1} -o 1.ass
0
Untitled-1.xml
test_init.py
-d 0
{file1} {file2} -O 1.ass"""
    for line in test.splitlines():
        argv = line.split(" ")
        code = run(argv)
        assert code == 1


def test_cli2():
    s = f"{file1} {file2} -l -x 1920 -y 1080 -f Microsoft -V -o ."
    argv = s.split(" ")
    code = run(argv)
    assert code == 0

    argv = [file1, "-O", "1.ass"]
    code = run(argv)
    assert code == 0

    argv = [file1, "-s"]
    code = run(argv)
    assert code == 0
