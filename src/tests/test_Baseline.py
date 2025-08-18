# -*- coding: utf-8 -*-

import difflib
import os

import pytest

from Annotations2Sub.cli import Run
from Annotations2Sub.utils import RedText, Stderr
from tests import baselinePath, testCasePath

baselines = [
    # 这个文件包含全部可能的结构和字段
    "annotations",
    # 这个文件有混乱数据案例
    "annotations2",
    "annotations3",
    # 这个视频是此项目的动机
    "e8kKeUuytqA",
    # 这个视频有复杂的气泡框
    "29-q7YnyUmY",
    # 这个视频是一个演示, 有大部分样式和需要换行的文本
    "M2ryDEyyrXE",
    # 这个视频有复杂的定位
    "g-0i6MOh7n0",
    "c1iCjpxDxz4",
]


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


@pytest.mark.parametrize("Baseline", baselines)
def test_baseline(Baseline: str):
    baseline_file = os.path.join(baselinePath, Baseline + ".xml.test")
    baseline_result = os.path.join(baselinePath, Baseline + ".ass.test")
    result = baseline_file + ".ass"

    Run(["-f", "Arial", baseline_file])
    assert equal(baseline_result, result)


@pytest.mark.parametrize("Baseline", baselines)
def test_baseline_transform(Baseline: str):
    baseline_file = os.path.join(baselinePath, Baseline + ".xml.test")
    baseline_result = os.path.join(baselinePath, Baseline + ".transform.ass.test")
    result = baseline_file + ".ass"

    Run(["-f", "Arial", "-x", "1920", "-y", "1080", baseline_file])
    assert equal(baseline_result, result)
