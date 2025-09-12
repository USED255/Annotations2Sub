# -*- coding: utf-8 -*-

from Annotations2Sub.flags import Flags


def test_flags():
    Flags.verbose = True
    assert Flags.verbose == True
