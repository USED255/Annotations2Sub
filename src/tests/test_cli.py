#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Annotations2Sub.cli import run

print(__file__)


def test_cli():
    code = run(["."])
    assert code == 1
