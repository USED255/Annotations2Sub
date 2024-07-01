import pytest

from Annotations2Sub.utils2 import GetAnnotationsUrl


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
