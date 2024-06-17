#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree

from Annotations2Sub import Convert, Parse, Sub
from Annotations2Sub.utils import _
from tests import garbagePath, testCasePath

filePath = os.path.join(testCasePath, "annotations.xml.test")
filePath2 = os.path.join(garbagePath, "annotations.ass.test")


def test_Annotations2Sub():
    with open(filePath, "r", encoding="utf-8") as f:
        string = f.read()
    tree = xml.etree.ElementTree.fromstring(string)
    annotations = Parse(tree)
    events = Convert(annotations, 1920, 1080)
    subtitle = Sub()
    subtitle.comment += _("此脚本使用 Annotations2Sub 生成") + "\n"
    subtitle.comment += "https://github.com/USED255/Annotations2Sub"
    subtitle.info["Title"] = "Annotations"
    subtitle.info["PlayResX"] = "1920"
    subtitle.info["PlayResY"] = "1080"
    subtitle.info["WrapStyle"] = "2"
    subtitle.events.extend(events)
    sub = subtitle.Dump()
    with open(filePath2, "w", encoding="utf-8") as f:
        f.write(sub)
