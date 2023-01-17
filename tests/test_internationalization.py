#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytest

from Annotations2Sub import tools


def test_internationalization():
    def a(*args, **kwargs):
        os.environ["LANG"] = ""

    m = pytest.MonkeyPatch()
    m.setattr(tools, "Dummy", a)
