#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

try:
    import Annotations2Sub
except:
    s1 = os.path.dirname(__file__)
    s2 = os.path.join(s1, "../src")
    s3 = os.path.abspath(s2)
    sys.path.append(s3)
import pytest

from Annotations2Sub.Color import Alpha, Color


def test_Alpha():
    with pytest.raises(ValueError):
        Alpha(256)


def test_Color():
    with pytest.raises(ValueError):
        Color(256, 0, 0)
    with pytest.raises(ValueError):
        Color(0, 256, 0)
    with pytest.raises(ValueError):
        Color(0, 0, 256)
