# Annotations2Sub

一个可以把Youtube注释转换成ASS字幕文件的脚本

A script that can convert Youtube Annotation into .ASS subtitles files

---

```man
usage: Annotations2Sub.py [-h] [-l] [-x 1920] [-y 1080] [-d] [-i invidious.domain] [-p] [-g] File or ID [File or ID ...]

A script that converts Youtube Annotations into .ASS subtitles

positional arguments:
  File or ID            The file to be converted

optional arguments:
  -h, --help            show this help message and exit
  -l, --libassHack      Fixes for libass
  -x 1920, --reset-resolution-x 1920
                        Reset resolution X
  -y 1080, --reset-resolution-y 1080
                        Reset resolution Y
  -d, --download-for-invidious
                        Try downloading the ‪‪annotations file from invidious
  -i invidious.domain, --invidious-domain invidious.domain
                        Specify invidious domain
  -p, --preview-video   Preview video(need mpv)
  -g, --generate-video  Generate video (need FFmpeg)

```

---

Example:

[Before](https://www.youtube.com/watch?v=e8kKeUuytqA)

```bash
python .\Annotations2Sub.py -g e8kKeUuytqA
```

[After](https://www.bilibili.com/video/BV1Ff4y1t7Dj?p=4)

---

[试例](https://www.used255.xyz/uploads/Annotations2Sub_试例)

---

TODO:

* ~~popup style~~
* ~~title style~~
* ~~speech style~~
* ~~highlightText style~~
* ~~libass hack~~
* ~~i18n~~
* ~~Download for invidious~~
* ~~Preview video~~
* ~~Generate video~~
* popup 行为
* speech 行为
* highlightText 行为
* Make Perfect
