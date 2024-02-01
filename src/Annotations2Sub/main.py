#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 程序入口 """

import sys
from typing import NoReturn

from Annotations2Sub.cli import Run


def main() -> NoReturn:
    sys.exit(Run())
