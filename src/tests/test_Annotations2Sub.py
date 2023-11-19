#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree

from Annotations2Sub.Annotation import Parse
from Annotations2Sub.Convert import Convert
from Annotations2Sub.Sub import Sub

filePath = os.path.join(os.path.dirname(__file__), "testCase", "annotation.xml.test")


def test_Annotations2Sub():
    with open(filePath, "r", encoding="utf-8") as f:
        string = f.read()
    tree = xml.etree.ElementTree.fromstring(string)
    annotations = Parse(tree)
    events = Convert(annotations, True)
    subtitle = Sub()
    subtitle.events.extend(events)
    subtitle.info["PlayResX"] = "100"
    subtitle.info["PlayResY"] = "100"
    subtitle.Dump()
