#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib
import os

from Annotations2Sub.cli import run
from Annotations2Sub.utils import RedText, Stderr

basePath = os.path.dirname(__file__)
testCasePath = os.path.join(basePath, "testCase")
baselinePath = os.path.join(testCasePath, "Baseline")

Baseline1 = os.path.join(baselinePath, "29-q7YnyUmY.xml.test")
Baseline2 = os.path.join(baselinePath, "e8kKeUuytqA.xml.test")

baseline1SSA = os.path.join(baselinePath, "29-q7YnyUmY.ass.test")
baseline2SSA = os.path.join(baselinePath, "e8kKeUuytqA.ass.test")


def equal(f1, f2):
    with open(f1, "r", encoding="utf-8") as f:
        a = f.readlines()
    with open(f2, "r", encoding="utf-8") as f:
        b = f.readlines()
    if a != b:
        differ = difflib.Differ()
        diffs = list(differ.compare(a, b))
        diffList = []
        for i in diffs:
            if i.startswith(" "):
                continue
            diffList.append(i)
        for i in diffList:
            Stderr(RedText(i))
        return False
    return True


def test_Baseline1():
    t = Baseline1 + ".ass"
    run([Baseline1])
    assert equal(t, baseline1SSA)


def test_Baseline2():
    t = Baseline2 + ".ass"
    run([Baseline2])
    assert equal(t, baseline2SSA)


def test_equal():
    assert not equal(
        os.path.join(testCasePath, "file1.test"),
        os.path.join(testCasePath, "file2.test"),
    )
