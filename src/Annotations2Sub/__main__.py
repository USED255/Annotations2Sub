#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 你也可以 python __main__.py 来使用本工具.
if not __package__:
    import os
    import sys

    path = os.path.abspath(os.path.split(os.path.realpath(__file__))[0])
    sys.path.append(path)
    path = os.path.abspath(os.path.join(path, os.pardir))
    sys.path.append(path)

from Annotations2Sub.cli import cli_entry

if __name__ == "__main__":
    cli_entry()
