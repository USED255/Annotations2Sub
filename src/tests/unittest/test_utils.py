# -*- coding: utf-8 -*-

from Annotations2Sub.utils import (
    Err,
    Err1,
    Err2,
    Info,
    RedText,
    Stderr,
    Warn,
    Warn1,
    Warn2,
    YellowText,
)


def test_YellowText():
    assert YellowText("Test") == "\033[33mTest\033[0m"


def test_RedText():
    assert RedText("Test") == "\033[31mTest\033[0m"


def test_Stderr():
    Stderr("Test")


def test_Err():
    Err("Test")


def test_Warn():
    Warn("Test")


def test_Info():
    Info("Test")


def test_Err1():
    Err1("Test")


def test_Warn1():
    Warn1("Test")


def test_Err2():
    Err2("Test")


def test_Warn2():
    Warn2("Test")
