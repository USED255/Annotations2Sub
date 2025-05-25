#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Annotations2Sub 应用程序的主要执行入口点。

当 `Annotations2Sub` 作为脚本运行或使用 `python -m Annotations2Sub` 调用时，
会调用此模块。它会（在直接运行时）设置必要的路径，
然后从 `cli` 模块调用主要的 `Run` 函数来启动应用程序。
"""

""" 程序入口 """

if not __package__:
    import os
    import sys

    path = os.path.abspath(os.path.split(os.path.realpath(__file__))[0])
    sys.path.append(path)
    path = os.path.abspath(os.path.join(path, os.pardir))
    sys.path.append(path)

import sys
from typing import NoReturn

from Annotations2Sub.cli import Run


def main() -> NoReturn:
    sys.exit(Run())


if __name__ == "__main__":
    main()
