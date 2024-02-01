#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib
import os

from Annotations2Sub.cli import Run
from Annotations2Sub.utils import RedText, Stderr

base_path = os.path.dirname(__file__)
test_case_path = os.path.join(base_path, "testCase")
baseline_path = os.path.join(test_case_path, "Baseline")

baseline1 = "annotations"
baseline2 = "e8kKeUuytqA"
baseline3 = "29-q7YnyUmY"


def equal(file1: str, file2: str) -> bool:
    with open(file1, "r", encoding="utf-8") as f:
        a = f.readlines()
    with open(file2, "r", encoding="utf-8") as f:
        b = f.readlines()
    if a != b:
        Stderr(RedText(file1))
        Stderr(RedText(file2))
        differ = difflib.Differ()
        diffs = list(differ.compare(a, b))
        for diff in diffs:
            if diff.startswith(" "):
                continue
            if diff.startswith("-"):
                Stderr("\n")
            if diff.startswith("?"):
                Stderr(RedText(diff))
                continue
            Stderr(diff)
        return False
    return True


def test_not_equal():
    assert not equal(
        os.path.join(test_case_path, "file1.test"),
        os.path.join(test_case_path, "file2.test"),
    )


def baseline(Baseline: str):
    baseline_file = os.path.join(baseline_path, Baseline + ".xml.test")
    baseline_result = os.path.join(baseline_path, Baseline + ".ass.test")
    result = baseline_file + ".ass"

    Run([baseline_file])
    assert equal(baseline_result, result)


def test_Baseline1():
    baseline(baseline1)


def test_Baseline2():
    baseline(baseline2)


def test_Baseline3():
    baseline(baseline3)


def baseline_transform(Baseline: str):
    baseline_file = os.path.join(baseline_path, Baseline + ".xml.test")
    baseline_result = os.path.join(baseline_path, Baseline + ".transform.ass.test")
    result = baseline_file + ".ass"

    Run([baseline_file, "-x", "1920", "-y", "1080"])
    assert equal(baseline_result, result)


def test_Baseline1_transform():
    baseline_transform(baseline1)


def test_Baseline2_transform():
    baseline_transform(baseline2)


def test_Baseline3_transform():
    baseline_transform(baseline3)
