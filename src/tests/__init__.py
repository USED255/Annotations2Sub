# -*- coding: utf-8 -*-

import os
import sys
import typing

import pytest

basePath = os.path.dirname(__file__)
testCasePath = os.path.join(basePath, "testCase")
garbagePath = os.path.join(basePath, "garbage")
baselinePath = os.path.join(testCasePath, "Baseline")

_m = pytest.MonkeyPatch()

_m.setenv("LC_ALL", "zh_CN")
_m.chdir(garbagePath)

if sys.version_info.major == 3 and sys.version_info.minor > 7:
    _m.delattr(typing, "Literal")

from Annotations2Sub.flags import Flags

Flags.verbose = True

"""
test_Baseline.py 的作用类似于回归测试,
确保修改不会意外破坏预期的行为.

test_cli.py 的作用类似于集成测试,
确保软件正常工作.

这两个测试覆盖了大部分代码.
"""
