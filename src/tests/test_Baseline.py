#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib
import os

from Annotations2Sub.cli import Run
from Annotations2Sub.utils import RedText, Stderr
from tests import testCasePath

baseline_path = os.path.join(testCasePath, "Baseline")

baselines = ["annotations", "e8kKeUuytqA", "29-q7YnyUmY"]


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
                Stderr("\n\n")
            if diff.startswith("?"):
                diff = diff.rstrip("\n")
                Stderr(RedText(diff))
                continue
            diff = diff.rstrip("\n")
            Stderr(diff)
        return False
    return True


def test_not_equal():
    assert not equal(
        os.path.join(testCasePath, "file1.test"),
        os.path.join(testCasePath, "file2.test"),
    )


def run_baseline(Baseline: str):
    baseline_file = os.path.join(baseline_path, Baseline + ".xml.test")
    baseline_result = os.path.join(baseline_path, Baseline + ".ass.test")
    result = baseline_file + ".ass"

    Run([baseline_file])
    assert equal(baseline_result, result)


def run_baseline_transform(Baseline: str):
    baseline_file = os.path.join(baseline_path, Baseline + ".xml.test")
    baseline_result = os.path.join(baseline_path, Baseline + ".transform.ass.test")
    result = baseline_file + ".ass"

    Run([baseline_file, "-x", "1920", "-y", "1080"])
    assert equal(baseline_result, result)


def test_baselines():
    for i in baselines:
        run_baseline(i)
        run_baseline_transform(i)
