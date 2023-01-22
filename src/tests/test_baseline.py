#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib
import os
import pytest

from Annotations2Sub.cli import run
from Annotations2Sub.tools import RedText, Stderr

path = os.path.dirname(__file__)
path1 = os.path.join(path, "Baseline")

file1 = os.path.join(path1, "29-q7YnyUmY.xml.test")
file2 = os.path.join(path1, "e8kKeUuytqA.xml.test")

baseline1 = os.path.join(path1, "29-q7YnyUmY.ass.test")
baseline2 = os.path.join(path1, "e8kKeUuytqA.ass.test")

m = pytest.MonkeyPatch()
m.setenv("LC_ALL","zh_CN")

def d(file1, file2):
    with open(file1, "r", encoding="utf-8") as f:
        a = f.read()
    with open(file2, "r", encoding="utf-8") as f:
        b = f.read()
    c = a.splitlines()
    d = b.splitlines()
    if c != d:
        d1 = difflib.Differ()
        diff = list(d1.compare(c, d))
        Stderr(RedText(str(diff)))
        return False
    return True


def test_1():
    t = file1 + ".ass"
    run([file1])
    assert d(t, baseline1)


def test_2():
    t = file2 + ".ass"
    run([file2])
    assert d(t, baseline2)


def test_3():
    assert not d(
        os.path.join(path, "test", "1.xml.test"),
        os.path.join(path, "test", "2.xml.test"),
    )
