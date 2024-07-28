# -*- coding: utf-8 -*-

import pytest

from Annotations2Sub.utils2 import (
    AnnotationsXmlStringToSubtitleString,
    GetAnnotationsUrl,
)


def test_GetAnnotationsUrl():
    assert (
        GetAnnotationsUrl("-8kKeUuytqA")
        == "https://archive.org/download/youtubeannotations_64/-8.tar/-8k/-8kKeUuytqA.xml"
    )


def test_GetAnnotationsUrl_ValueError():
    with pytest.raises(ValueError):
        GetAnnotationsUrl("")


def test_GetMedia():
    pass


def test_AnnotationsXmlStringToSubtitleString():
    pass


def test_AnnotationsXmlStringToSubtitleString_ValueError():
    with pytest.raises(ValueError):
        AnnotationsXmlStringToSubtitleString("")
