#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""程序入口"""

import sys
import traceback
from typing import NoReturn

from Annotations2Sub.cli import Run
from Annotations2Sub.i18n import _
from Annotations2Sub.utils import Err, Stderr
from Annotations2Sub.windows import tips_double_clicked_on_windows


def main() -> NoReturn:
    try:
        code = Run()
    except SystemExit:
        code = 2
    except:
        Stderr(traceback.format_exc())
        Err(_("出现未知错误"))
        code = 19

    tips_double_clicked_on_windows()
    sys.exit(code)
