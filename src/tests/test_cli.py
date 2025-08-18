# -*- coding: utf-8 -*-

import os
from typing import Tuple

import pytest

from Annotations2Sub.cli import Run
from Annotations2Sub.utils import Stderr
from tests import baselinePath, testCasePath

baseline1_file = os.path.join(baselinePath, "29-q7YnyUmY.xml.test")
baseline2_file = os.path.join(baselinePath, "e8kKeUuytqA.xml.test")

empty_xml = os.path.join(testCasePath, "empty.xml.test")
empty_annotations = os.path.join(testCasePath, "emptyAnnotations.xml.test")
file1 = os.path.join(testCasePath, "file1.test")


test_set = [
    # 预期成功的命令
    (f"{baseline1_file} {baseline2_file} -x 1080 -y 1920 -f Microsoft -V -O .", 0),
    (f"{baseline1_file} -o annotations.ass", 0),
    (f"{baseline1_file} -o -", 0),
    (f"{baseline1_file} -n", 0),
    (f"{empty_annotations}", 0),
    # 预期失败的命令
    (f"-ND {baseline1_file}", 11),
    (f"{baseline1_file} -O {file1}", 2),
    (f"{baseline1_file} {baseline2_file} -o 1.ass", 2),
    (f"{baseline1_file} -O . -o 1.ass", 2),
    (f"{empty_xml}", 14),
    (f"{file1}", 15),
    (f"0", 13),
    (f"-d 0", 11),
]


@pytest.mark.parametrize("testSet", test_set)
def test_cli(testSet: Tuple[str, int]):
    argument = testSet[0]
    expect_code = testSet[1]

    Stderr(argument)
    argv = argument.split(" ")
    code = Run(argv)
    assert expect_code == code
