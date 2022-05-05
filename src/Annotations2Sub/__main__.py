#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

if __name__ == "__main__":
    path = os.path.split(os.path.realpath(__file__))[0]
    sys.path.append(path)
    path = os.path.abspath(os.path.join('path', os.pardir))
    sys.path.append(path)
    from Annotations2Sub.cli import main

    main()
