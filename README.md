# Annotations2Sub

一个可以把 Youtube 注释转换成 ASS(Advanced SubStation Alpha) 字幕文件的脚本

A script that can convert Youtube Annotation into ASS(Advanced SubStation Alpha) subtitles files

[![License GPLv3](https://img.shields.io/pypi/l/Annotations2Sub?color=1)](https://pypi.org/project/Annotations2Sub/)
[![Test](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml/badge.svg)](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/USED255/Annotations2Sub/branch/master/graph/badge.svg?token=SSNQNEAXMP)](https://codecov.io/gh/USED255/Annotations2Sub)
[![Version](https://img.shields.io/pypi/v/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)
[![Python version](https://img.shields.io/pypi/pyversions/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)

---

```bash
pip install Annotations2Sub
```

```help
usage: Annotations2Sub.py [-h] [-l] [-x 100] [-y 100] [-f Microsoft YaHei] [-d]
                          [-i invidious-instances.domain] [-p] [-g] [-u] [-v] [-V]
                          File or videoId [File or videoId ...]

A script that converts Youtube Annotations into ASS(Advanced SubStation Alpha) subtitles file

positional arguments:
  File or videoId       File path of multiple files to be converted, or multiple
                        Youtube videoId to be previewed, generated, Annotations file 
                        downloaded from Internet Archive

optional arguments:
  -h, --help            Show this help message and exit
  -l, --embrace-libass  Embrace libass's quirks and features, and not specifying
                        This option will adapt to xy-vsfilter
  -x 100, --transform-resolution-x 100
                        Transform resolution X
  -y 100, --transform-resolution-y 100
                        Transform resolution Y
  -f Arial, --font Arial
                        Specify font
  -o Folder, --output-directory Folder
                        Specify the output path of the converted file,
                        not specifying this option will output the converted
                        file to the same directory as the converted file
  -d, --download-for-archive
                        Try downloading the annotations file from Internet Archive
  -i invidious-instances.domain, --invidious-instances invidious-instances.domain
                        Specify invidious instances (https://redirect.invidious.io/)
  -p, --preview-video   Preview video, need mpv(https://mpv.io/) and specify invidious instances
  -g, --generate-video  Generate video, need FFmpeg(https://ffmpeg.org/) and specify invidious instances
  -s, --output-to-stdout
                        Output to stdout
  -n, --no-overwrite-files
                        No file overwriting
  -k, --no-keep-intermediate-files
                        No retention of intermediate files
  -u, --unstable        Enabling Unstable function, can cause some problems
  -v, --version         Show version
  -V, --verbose         Show more messages
```

---

Example:

[Before](https://www.youtube.com/watch?v=HqSzHYxVKws)

```bash
Annotations2Sub.py -g HqSzHYxVKws
```

[After](https://www.bilibili.com/video/BV1Ff4y1t7Dj)

---

如果效果不对, 欢迎 issue

If it doesn't work right, feel free to issue

---
