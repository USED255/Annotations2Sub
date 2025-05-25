#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main execution entry point for the Annotations2Sub application.

This module is invoked when `Annotations2Sub` is run as a script or
using `python -m Annotations2Sub`. It sets up the necessary paths
(if run directly) and then calls the main `Run` function from the
`cli` module to start the application.
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
