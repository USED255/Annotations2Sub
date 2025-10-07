# -*- coding: utf-8 -*-

import sys
import traceback
from typing import NoReturn

from Annotations2Sub.cli import Run
from Annotations2Sub.i18n import _
from Annotations2Sub.utils import Err, Stderr


def main() -> NoReturn:
    """程序入口"""
    try:
        code = Run()
    except SystemExit:
        code = 2
    except:
        Stderr(traceback.format_exc())
        Err(_("出现未知错误"))
        code = 19

    sys.exit(code)
