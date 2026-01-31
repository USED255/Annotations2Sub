# -*- coding: utf-8 -*-

import pytest

import Annotations2Sub.__main__


def test_main():
    with pytest.raises(SystemExit):
        Annotations2Sub.__main__.main()
