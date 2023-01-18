#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

try:
    import Annotations2Sub
except:
    s1 = os.path.dirname(__file__)
    s2 = os.path.join(s1, "../src")
    s3 = os.path.abspath(s2)
    sys.path.append(s3)
import os
import xml.etree.ElementTree

from Annotations2Sub.Annotation import Parse
from Annotations2Sub.Convert import Convert
from Annotations2Sub.tools import Flags
from Annotations2Sub.Sub import Sub


def test_Annotations2Sub():
    Flags.verbose = True
    Flags.unstable = True
    filePath = os.path.join(os.path.dirname(__file__), "xml.test")
    with open(filePath, "r", encoding="utf-8") as f:
        string = f.read()
    tree = xml.etree.ElementTree.fromstring(string)
    annotations = Parse(tree)
    events = Convert(annotations, True)
    sub = Sub()
    sub.events.extend(events)
    sub.info["PlayResX"] = "100"
    sub.info["PlayResY"] = "100"
    sub.Dump()
