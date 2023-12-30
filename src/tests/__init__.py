#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import typing

import pytest

basePath = os.path.dirname(__file__)
testCasePath = os.path.join(basePath, "testCase")
garbagePath = os.path.join(testCasePath, "garbage")

m = pytest.MonkeyPatch()

m.setenv("LC_ALL", "zh_CN")
m.chdir(garbagePath)

if sys.version_info.major == 3 and sys.version_info.minor > 7:
    m.delattr(typing, "Literal")

from Annotations2Sub.utils import Flags

Flags.verbose = True
