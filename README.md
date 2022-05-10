# Annotations2Sub

一个可以把 Youtube 注释转换成 ASS(Sub Station Alpha V4) 字幕文件的脚本

A script that can convert Youtube Annotation into ASS(Sub Station Alpha V4) subtitles files

---

```bash
pip install Annotations2Sub
```

```help
usage: Annotations2Sub.py [-h] [-l] [-x 100] [-y 100] [-f Microsoft YaHei] [-d]
                          [-i invidious-instances.domain] [-p] [-g] [-u] [-v] [-V]
                          File or videoId [File or videoId ...]

A script that converts Youtube Annotations into ASS(Sub Station Alpha V4) subtitles file

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
  -o File, --output File
                        Specify the output path of the converted file,
                        not specifying this option will output the converted
                        file to the same directory as the converted file
  -d, --download-for-archive
                        Try downloading the annotations file from Internet Archive
  -i invidious-instances.domain, --invidious-instances invidious-instances.domain
                        Specify invidious instances (https://redirect.invidious.io/)
  -p, --preview-video   Preview video, need mpv(https://mpv.io/) and 
                        specify invidious instances
  -g, --generate-video  Generate video, need FFmpeg(https://ffmpeg.org/) and 
                        specify invidious instances
  -u, --unstable        Enabling Unstable function, such as speech style, 
                        highlightText style, can cause some problems
  -v, --version         Show version
  -V, --verbose         Show a lot messages
```

Example:

[Before](https://www.youtube.com/watch?v=HqSzHYxVKws)

```bash
Annotations2Sub.py -g HqSzHYxVKws
```

[After](https://www.bilibili.com/video/BV1Ff4y1t7Dj)

---
