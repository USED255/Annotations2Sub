#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Annotations2Sub.tools import AnnotationsForArchive, RedText, YellowText


def test_YellowText():
    assert YellowText("Test") == "\033[33mTest\033[0m"

def test_RedText():
    assert RedText("Test") == "\033[31mTest\033[0m"

def test_AnnotationsForArchive():
    assert AnnotationsForArchive("e8kKeUuytqA") == "https://archive.org/download/youtubeannotations_30/e8.tar/e8k/e8kKeUuytqA.xml"

