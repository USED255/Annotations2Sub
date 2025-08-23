# -*- coding: utf-8 -*-

import os

import pytest

from Annotations2Sub.cli import Run
from Annotations2Sub.utils import Stderr
from tests import baselinePath, testCasePath

baseline1_file = os.path.join(baselinePath, "29-q7YnyUmY.xml.test")
baseline2_file = os.path.join(baselinePath, "e8kKeUuytqA.xml.test")

empty_xml = os.path.join(testCasePath, "empty.xml.test")
empty_annotations = os.path.join(testCasePath, "emptyAnnotations.xml.test")
file1 = os.path.join(testCasePath, "file1.test")
empty_file = os.path.join(testCasePath, "empty.test")

"""
0: 成功
2: 参数错误
11: 无效视频ID
13: 不是文件
14: 不是 Annotations 文件
15: 无效的 XML 文档
18: 多个错误
20: 空文件
"""

test_set = [
    # 预期成功的命令
    (f"{baseline1_file} {baseline2_file} -x 1080 -y 1920 -f Microsoft -V -O .", 0),
    (f"{baseline1_file} -o annotations.ass", 0),
    (f"{baseline1_file} -o -", 0),
    (f"{baseline1_file} -n", 0),
    (f"{empty_annotations}", 0),
    # 预期失败的命令
    (f"-ND {baseline1_file}", 11),
    # 输出目录不能是一个文件
    (f"{baseline1_file} -O {file1}", 2),
    # 多个文件不能输出到一个文件
    (f"{baseline1_file} {baseline2_file} -o 1.ass", 2),
    # "-O" 和 "-o" 不能一起用
    (f"{baseline1_file} -O . -o 1.ass", 2),
    (f"{empty_xml}", 14),
    (f"{file1}", 15),
    ("0", 13),
    ("-d 0", 11),
    ("0 0", 18),
    (f"{empty_file}", 20),
]


@pytest.mark.parametrize("Argument, ExitCode", test_set)
def test_cli(Argument: str, ExitCode: int):
    Stderr(Argument)
    args = Argument.split(" ")
    code = Run(args)
    assert ExitCode == code
