#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if not __package__:
    import os
    import sys

    path = os.path.abspath(os.path.split(os.path.realpath(__file__))[0])
    sys.path.append(path)
    path = os.path.abspath(os.path.join(path, os.pardir))
    sys.path.append(path)

from Annotations2Sub._main import main

if __name__ == "__main__":
    main()
