#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""python __main__.py"""

import os
import sys

if __name__ == "__main__":
    # 从 youtube-dl 的 __main__.py 学来的
    # 为了可以直接 python __main__.py
    # 不过大概率不会用到这些
    path = os.path.abspath(os.path.split(os.path.realpath(__file__))[0])
    sys.path.append(path)
    path = os.path.abspath(os.path.join(path, os.pardir))
    sys.path.append(path)
    from Annotations2Sub.main import main

    main()
