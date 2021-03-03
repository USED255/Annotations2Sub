# Annotations2Sub

一个可以把Youtube注释转换成ASS字幕文件的脚本

A script that can convert Youtube Annotation into .ASS subtitles files

---

```
usage: Annotations2Sub.py [-h] [-l] [-d] [-i invidious.domain] [-p] [-g] File or ID [File or ID ...]

A script that converts Youtube Annotations into .ASS subtitles

positional arguments:
  File or ID            The file to be converted

optional arguments:
  -h, --help            show this help message and exit
  -l, --libassHack      Fixes for libass
  -d, --download-for-invidious
                        Try downloading the ‪‪annotations file from invidious
  -i invidious.domain, --invidious-domain invidious.domain
                        Specify invidious domain
  -p, --preview-video   Preview video(need ffplay or mpv)

```

[试例](https://www.used255.xyz/uploads/Annotations2Sub_试例)

---

TODO:

* <del>popup style </del>
* <del>title style </del>
* speech style 
* highlightText style
* None style
* <del>libass hack</del>
* <del>i18n</del>
* <del>Download for invidious</del>
* Rewrite _convert()
* <del>Preview video</del>
* Generate video
* Other style 
