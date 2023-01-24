#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib
import os

from Annotations2Sub.cli import run
from Annotations2Sub.utils import RedText, Stderr

path = os.path.dirname(__file__)
path1 = os.path.join(path, "Baseline")

file1 = os.path.join(path1, "29-q7YnyUmY.xml.test")
file2 = os.path.join(path1, "e8kKeUuytqA.xml.test")

baseline1 = os.path.join(path1, "29-q7YnyUmY.ass.test")
baseline2 = os.path.join(path1, "e8kKeUuytqA.ass.test")


def d(f1, f2):
    with open(f1, "r", encoding="utf-8") as f:
        a = f.readlines()
    with open(f2, "r", encoding="utf-8") as f:
        b = f.readlines()
    if a != b:
        d1 = difflib.Differ()
        diff = list(d1.compare(a, b))
        d2 = []
        for i in diff:
            if i.startswith(" "):
                continue
            d2.append(i)
        for i in d2:
            Stderr(RedText(i))
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
