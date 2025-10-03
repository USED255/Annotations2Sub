# -*- coding: utf-8 -*-

# 兼容 Python 3.7
# Python 3.7 的 typing 没有 Literal
try:
    from typing import Literal
except ImportError:

    class a:
        def __getitem__(self, b):
            return b

    exec("Literal = a()")

accuracy = 3


def _round(x: float) -> float:
    return round(x, accuracy)
