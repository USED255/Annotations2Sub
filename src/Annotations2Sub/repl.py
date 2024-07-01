import os

from Annotations2Sub.i18n import _
from Annotations2Sub.utils2 import AnnotationsXmlStringToSubtitleString


def AnnotationsXmlFileToSubtitleFile(
    annotations_file: str,
    output_file: str,
    transform_resolution_x: int = 100,
    transform_resolution_y: int = 100,
    font="Microsoft YaHei",
):
    if os.path.isfile(annotations_file) is False:
        raise FileNotFoundError(_('"{}" 不是一个文件').format(annotations_file))

    with open(annotations_file, "r", encoding="utf-8") as f:
        annotations_string = f.read()

    subtitle_string = AnnotationsXmlStringToSubtitleString(
        annotations_string,
        transform_resolution_x,
        transform_resolution_y,
        font,
        os.path.basename(annotations_file),
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(subtitle_string)
