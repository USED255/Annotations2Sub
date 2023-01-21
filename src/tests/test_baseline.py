#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib

from Annotations2Sub.cli import run

path = os.path.dirname(__file__)
path = os.path.join(path, "Baseline")

file1 = os.path.join(path, "29-q7YnyUmY.xml.test")
file2 = os.path.join(path, "e8kKeUuytqA.xml.test")

baseline1 = os.path.join(path, "29-q7YnyUmY.xml.ass.test")
baseline2 = os.path.join(path, "e8kKeUuytqA.xml.ass.test")


def d(file1, file2):
    with open(file1, "rb") as f:
        a = hashlib.sha256(f.read()).digest()
    with open(file2, "rb") as f:
        b = hashlib.sha256(f.read()).digest()
    return a == b


def test_1():
    t = file1 + ".ass"
    run([file1])
    assert d(t, baseline1)


def test_2():
    t = file2 + ".ass"
    run([file2])
    assert d(t, baseline2)
