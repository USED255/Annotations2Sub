# -*- coding: utf-8 -*-
import os

import pytest

from Annotations2Sub import cli_utils
from Annotations2Sub.cli_utils import AnnotationsXmlStringToSub, GetAnnotationsUrl
from tests import testCasePath


def test_GetAnnotationsUrl():
    assert (
        GetAnnotationsUrl("-8kKeUuytqA")
        == "https://archive.org/download/youtubeannotations_64/-8.tar/-8k/-8kKeUuytqA.xml"
    )


def test_GetAnnotationsUrl_ValueError():
    with pytest.raises(ValueError):
        GetAnnotationsUrl("")


def test_GetMedia():
    def GetUrlMock(url: str):
        if url == "https://good.instance/api/v1/videos/-8kKeUuytqA":
            return r'{"adaptiveFormats":[{"type":"video","bitrate":1,"url":"https://1/video"},{"type":"audio","bitrate":1,"url":"https://1/audio"}]}'

    m = pytest.MonkeyPatch()
    m.setattr(cli_utils, "GetUrl", GetUrlMock)

    assert cli_utils.GetMedia("-8kKeUuytqA", "good.instance") == (
        "https://1/video",
        "https://1/audio",
    )

    m.undo()


def test_AnnotationsXmlStringToSub():
    file = os.path.join(testCasePath, "annotations.xml.test")
    with open(file) as f:
        assert AnnotationsXmlStringToSub(f.read())


def test_AnnotationsXmlStringToSub_ValueError():
    with pytest.raises(ValueError):
        AnnotationsXmlStringToSub("")
