#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import pytest

basePath = os.path.dirname(__file__)
testCasePath = os.path.join(basePath, "testCase")
garbagePath = os.path.join(testCasePath, "garbage")

m = pytest.MonkeyPatch()
m.setenv("LC_ALL", "zh_CN")

m.chdir(garbagePath)

from Annotations2Sub.utils import Flags

Flags.verbose = True
