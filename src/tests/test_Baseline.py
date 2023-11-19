#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib
import os

from Annotations2Sub.cli import run
from Annotations2Sub.utils import RedText, Stderr

base_path = os.path.dirname(__file__)
test_case_path = os.path.join(base_path, "testCase")
baseline_path = os.path.join(test_case_path, "Baseline")

baseline1 = os.path.join(baseline_path, "29-q7YnyUmY.xml.test")
baseline2 = os.path.join(baseline_path, "e8kKeUuytqA.xml.test")
baseline3 = os.path.join(baseline_path, "annotation.xml.test")

baseline1_ssa = os.path.join(baseline_path, "29-q7YnyUmY.ass.test")
baseline2_ssa = os.path.join(baseline_path, "e8kKeUuytqA.ass.test")
baseline3_ssa = os.path.join(baseline_path, "annotation.ass.test")


def equal(file1: str, file2: str) -> bool:
    with open(file1, "r", encoding="utf-8") as f:
        a = f.readlines()
    with open(file2, "r", encoding="utf-8") as f:
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


def test_equal():
    assert not equal(
        os.path.join(test_case_path, "file1.test"),
        os.path.join(test_case_path, "file2.test"),
    )


def test_Baseline1():
    target = baseline1 + ".ass"
    run([baseline1])
    assert equal(baseline1_ssa, target)


def test_Baseline2():
    target = baseline2 + ".ass"
    run([baseline2])
    assert equal(baseline2_ssa, target)


def test_Baseline3():
    target = baseline3 + ".ass"
    run([baseline3])
    assert equal(baseline3_ssa, target)
