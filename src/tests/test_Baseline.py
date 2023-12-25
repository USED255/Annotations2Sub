#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib
import os

from Annotations2Sub.cli import Run
from Annotations2Sub.utils import RedText, Stderr

base_path = os.path.dirname(__file__)
test_case_path = os.path.join(base_path, "testCase")
baseline_path = os.path.join(test_case_path, "Baseline")

baseline1 = "29-q7YnyUmY"
baseline2 = "e8kKeUuytqA"
baseline3 = "annotations"

baseline1_file = os.path.join(baseline_path, baseline1 + ".xml.test")
baseline2_file = os.path.join(baseline_path, baseline2 + ".xml.test")
baseline3_file = os.path.join(baseline_path, baseline3 + ".xml.test")

baseline1_ssa = os.path.join(baseline_path, baseline1 + ".ass.test")
baseline2_ssa = os.path.join(baseline_path, baseline2 + ".ass.test")
baseline3_ssa = os.path.join(baseline_path, baseline3 + ".ass.test")

baseline1_transform = os.path.join(baseline_path, baseline1 + ".transform.ass.test")
baseline2_transform = os.path.join(baseline_path, baseline2 + ".transform.ass.test")
baseline3_transform = os.path.join(baseline_path, baseline3 + ".transform.ass.test")


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


def test_not_equal():
    assert not equal(
        os.path.join(test_case_path, "file1.test"),
        os.path.join(test_case_path, "file2.test"),
    )


def test_Baseline1():
    target = baseline1_file + ".ass"
    Run([baseline1_file])
    assert equal(baseline1_ssa, target)
    Run([baseline1_file, "-x", "1920", "-y", "1080"])
    assert equal(baseline1_transform, target)


def test_Baseline2():
    target = baseline2_file + ".ass"
    Run([baseline2_file])
    assert equal(baseline2_ssa, target)
    Run([baseline2_file, "-x", "1920", "-y", "1080"])
    assert equal(baseline2_transform, target)


def test_Baseline3():
    target = baseline3_file + ".ass"
    Run([baseline3_file])
    assert equal(baseline3_ssa, target)

    Run([baseline3_file, "-x", "1920", "-y", "1080"])
    assert equal(baseline3_transform, target)
