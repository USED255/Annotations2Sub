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
  File or videoId       Multiple files that need to be converted or
                        videoId's that need to be previewed or generated
                        for Youtube videos

optional arguments:
  -h, --help            show this help message and exit
  -l, --use-libass      fixes for libass
  -x 100, --transform-resolution-x 100
                        transform resolution X
  -y 100, --transform-resolution-y 100
                        transform resolution Y
  -f Microsoft YaHei UI, --font Microsoft YaHei UI 
                        specify font
  -d, --download-for-archive
                        Try downloading the annotations file from Internet Archive
  -i invidious-instances.domain, --invidious-domain invidious-instances.domain
                        Specify invidious instances
  -p, --preview-video   preview video, need mpv and specify invidious domain
  -g, --generate-video  generate video, need FFmpeg and specify invidious domain
  -u, --unstable        unstable function
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
