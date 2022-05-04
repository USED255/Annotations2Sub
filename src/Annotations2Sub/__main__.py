#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

if __name__ == "__main__":
    sys.path.append(os.path.split(os.path.realpath(__file__))[0])
    from Annotations2Sub.cli import main

    main()
