#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import filecmp
import os

from Annotations2Sub.cli import run

path = os.path.dirname(__file__)
path = os.path.join(path, "Baseline")

file1 = os.path.join(path, "29-q7YnyUmY.xml.test")
file2 = os.path.join(path, "e8kKeUuytqA.xml.test")

baseline1 = os.path.join(path, "29-q7YnyUmY.xml.ass.test")
baseline2 = os.path.join(path, "e8kKeUuytqA.xml.ass.test")


def test_1():
    run([file1])
    assert filecmp.cmp(file1 + ".ass", baseline1)


def test_2():
    run([file2])
    assert filecmp.cmp(file2 + ".ass", baseline2)
