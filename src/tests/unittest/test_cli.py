# -*- coding: utf-8 -*-

import pytest

from Annotations2Sub.cli import Run


def test_Run():
    with pytest.raises(SystemExit):
        Run([])
