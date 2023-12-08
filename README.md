# Annotations2Sub

下载和转换 Youtube 注释

Download and convert Youtube Annotation

[![License GPLv3](https://img.shields.io/pypi/l/Annotations2Sub?color=1)](https://pypi.org/project/Annotations2Sub/)
[![Test](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml/badge.svg)](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/USED255/Annotations2Sub/branch/master/graph/badge.svg?token=SSNQNEAXMP)](https://codecov.io/gh/USED255/Annotations2Sub)
[![Version](https://img.shields.io/pypi/v/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)
[![Python version](https://img.shields.io/pypi/pyversions/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)

---

**因为字幕滤镜行为和怪癖的不断变动, 以及Web技术和字幕技术上的巨大差异, 本项目无法正确还原注释的行为**

**Because of the constant changes in subtitle filter behavior and quirks, as well as the huge differences in web technology and subtitle technology, this project was unable to correctly restore the behavior of annotations.**

```bash
pip install Annotations2Sub
```

```help
usage: Annotations2Sub.py [-h] [-l] [-x 100] [-y 100] [-f Arial ] [-o Folder] [-d]
                          [-i invidious.domain] [-p] [-g] [-s] [-n] [-k] [-u] [-v]
                          [-V]
                          File or videoId [File or videoId ...]

Download and convert Youtube Annotation

positional arguments:
  File or videoId       File path or video ID of multiple files to be convert

optional arguments:
  -h, --help            Show this help message and exit
  -l, --embrace-libass  Embrace libass's quirks and features, and not specifying
                        this option will adapt to xy-vsfilter
  -x 100, --transform-resolution-x 100
                        Transform resolution X
  -y 100, --transform-resolution-y 100
                        Transform resolution Y
  -f Arial, --font Arial
                        Specify font
  -d, --download-for-archive
                        Try to download the Annotations file from Internet Archive
  -D, --download-annotation-only
                        Download Annotation only
  -p, --preview-video   Preview video, requires mpv(https://mpv.io/)
  -g, --generate-video  Generate video, requires FFmpeg(https://ffmpeg.org/)
  -i invidious-instances.domain, --invidious-instances invidious-instances.domain
                        Specify invidious instances (https://redirect.invidious.io/)
  -n, --no-overwrite-files
                        Do not overwrite files
  -N, --no-keep-intermediate-files
                        Do not keep intermediate files
  -O directory, --output-directory directory
                        Specify the output directory for the converted file
  -o File, --output File
                        Save to this file, if "-" then output to standard output
  -v, --version         Show version
  -V, --verbose         Show more messages
```

---

转换注释文件

Convert Annotation

```bash
Annotations2Sub 29-q7YnyUmY.xml
```

下载并转换注释文件

Download and convert Annotation

```bash
Annotations2Sub -d 29-q7YnyUmY
```

生成视频

Generate video

```bash
Annotations2Sub -g 29-q7YnyUmY
```
