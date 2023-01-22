#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

m = pytest.MonkeyPatch()
m.setenv("LC_ALL", "zh_CN")
