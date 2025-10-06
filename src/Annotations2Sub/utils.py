# -*- coding: utf-8 -*-

import sys

from Annotations2Sub.flags import Flags
from Annotations2Sub.i18n import _


def YellowText(string: str) -> str:
    return f"\033[33m{string}\033[0m"


def RedText(string: str) -> str:
    return f"\033[31m{string}\033[0m"


def Stderr(string: str):
    print(string, file=sys.stderr)


def Err1(string: str):
    Stderr(RedText(string))


def Warn1(string: str):
    Stderr(YellowText(string))


def Err2(string: str):
    Stderr(_("错误: ") + string)


def Warn2(string: str):
    Stderr(_("警告: ") + string)


def Info(string: str):
    if Flags.verbose:
        Stderr(string)


Err = Err1
Warn = Warn1

if not sys.stdout.isatty():
    Err = Err2
    Warn = Warn2
