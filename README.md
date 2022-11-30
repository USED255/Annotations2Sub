# Annotations2Sub

下载和转换 Youtube 注释

Download and convert Youtube Annotation

[![License GPLv3](https://img.shields.io/pypi/l/Annotations2Sub?color=1)](https://pypi.org/project/Annotations2Sub/)
[![Test](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml/badge.svg)](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/28155e10849a40eb8d02f341073f2901)](https://www.codacy.com/gh/USED255/Annotations2Sub/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=USED255/Annotations2Sub&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/USED255/Annotations2Sub/branch/master/graph/badge.svg?token=SSNQNEAXMP)](https://codecov.io/gh/USED255/Annotations2Sub)
[![Version](https://img.shields.io/pypi/v/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)
[![Python version](https://img.shields.io/pypi/pyversions/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)

---

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
  File or videoId       File path of multiple files to be converted, or multiple
                        Youtube videoId to be previewed, generated, Annotations
                        file downloaded from Internet Archive

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
  -d, --download-for-archive
                        Try downloading the annotations file from Internet Archive
  -p, --preview-video   Preview video, need mpv(https://mpv.io/) and specify 
                        invidious instances
  -g, --generate-video  Generate video, need FFmpeg(https://ffmpeg.org/) and specify
                        invidious instances
  -i invidious-instances.domain, --invidious-instances invidious-instances.domain
                        Specify invidious instances (https://redirect.invidious.io/)
  -s, --output-to-stdout
                        Output to stdout
  -n, --no-overwrite-files
                        No file overwriting
  -N, --no-keep-intermediate-files
                        No retention of intermediate files
  -o Folder, --output-directory Folder
                        Specify the output path of the converted file, not
                        specifying this option will output the converted file
                        to the same directory as the converted file
  -O File, --output File
                        Save to this file
  -S, --skip-invalid-files
                        Skip invalid files
  -u, --unstable        Enabling Unstable function, can cause some problems
  -v, --version         Show version
  -V, --verbose         Show more messages
```

---

转换注释文件

```bash
Annotations2Sub 29-q7YnyUmY.xml
```

下载并转换注释文件

```bash
Annotations2Sub -d 29-q7YnyUmY
```

生成视频

```bash
Annotations2Sub -g 29-q7YnyUmY
```
