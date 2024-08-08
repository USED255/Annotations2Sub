#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 程序入口 """

import sys
from typing import NoReturn

from Annotations2Sub.cli import Run


def main() -> NoReturn:
    sys.exit(Run())


if not __package__:
    import os
    import sys

    path = os.path.abspath(os.path.split(os.path.realpath(__file__))[0])
    sys.path.append(path)
    path = os.path.abspath(os.path.join(path, os.pardir))
    sys.path.append(path)

if __name__ == "__main__":
    main()
