# -*- coding: utf-8 -*-

import os

from Annotations2Sub.cli import Run
from Annotations2Sub.utils import Stderr
from tests import baselinePath, testCasePath

baseline1_file = os.path.join(baselinePath, "29-q7YnyUmY.xml.test")
baseline2_file = os.path.join(baselinePath, "e8kKeUuytqA.xml.test")

empty_xml = os.path.join(testCasePath, "empty.xml.test")
empty_annotations = os.path.join(testCasePath, "emptyAnnotations.xml.test")
file1 = os.path.join(testCasePath, "file1.test")


def test_cli_failed():
    """预期失败的命令"""
    commands = f"""-ND {baseline1_file}
{baseline1_file} -O {file1}
{baseline1_file} {baseline2_file} -o 1.ass
{baseline1_file} -O . -o 1.ass
{empty_xml}
{file1}
0
-d 0"""

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = Run(argv)
        assert code != 0


def test_cli_success():
    """预期成功的命令"""
    commands = f"""{baseline1_file} {baseline2_file} -x 1080 -y 1920 -f Microsoft -V -O .
{baseline1_file} -o annotations.ass
{baseline1_file} -o -
{baseline1_file} -n
{empty_annotations}"""

    for command in commands.splitlines():
        Stderr(command)
        argv = command.split(" ")
        code = Run(argv)
        assert code == 0
