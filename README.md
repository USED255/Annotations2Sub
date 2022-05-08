# Annotations2Sub

一个可以把 Youtube 注释转换成 ASS(Sub Station Alpha V4) 字幕文件的脚本

A script that can convert Youtube Annotation into ASS(Sub Station Alpha V4) subtitles files

---

```bash
pip install Annotations2Sub
```

```man
usage: Annotations2Sub.py [-h] [-l] [-x 100] [-y 100] [-f Microsoft YaHei] [-d]
                          [-i invidious-instances.domain] [-p] [-g] [-u] [-v] [-V]
                          File or videoId [File or videoId ...]

A script that converts Youtube Annotations into ASS(Sub Station Alpha V4) subtitles file

positional arguments:
  File or videoId       File path of multiple files to be converted, or multiple
                        Youtube videoId to be previewed, generated, Annotations file 
                        downloaded from Internet Archive

optional arguments:
  -h, --help            show this help message and exit
  -l, --embrace-libass  embrace libass's quirks and features, and not specifying
                        this option will adapt to xy-vsfilter
  -x 100, --transform-resolution-x 100
                        transform resolution X
  -y 100, --transform-resolution-y 100
                        transform resolution Y
  -f Arial, --font Arial
                        specify font
  -o File, --output File
                        specify the output path of the converted file,
                        not specifying this option will output the converted
                        file to the same directory as the converted file
  -d, --download-for-archive
                        Try downloading the annotations file from Internet Archive
  -i invidious-instances.domain, --invidious-domain invidious-instances.domain
                        Specify invidious instances
  -p, --preview-video   preview video, need mpv and specify invidious domain
  -g, --generate-video  generate video, need FFmpeg and specify invidious domain
  -u, --unstable        unstable function, like speech and highlightText
  -v, --version         show version
  -V, --verbose         show a lot messages
```

Example:

[Before](https://www.youtube.com/watch?v=HqSzHYxVKws)

```bash
Annotations2Sub.py -g HqSzHYxVKws
```

[After](https://www.bilibili.com/video/BV1Ff4y1t7Dj)

---
