# Annotations2Sub

一个可以把 Youtube 注释转换成 ASS(Sub Station Alpha V4) 字幕文件的脚本

A script that can convert Youtube Annotation into ASS(Sub Station Alpha V4) subtitles files

---

```bash
pip install Annotations2Sub
```

```man
usage: Annotations2Sub.py [-h] [-l] [-x 100] [-y 100] [-f Microsoft YaHei UI] [-d] [-i invidious-instances.domain] [-p] [-g] 
                          File or videoId [File or videoId ...]

A script that converts Youtube Annotations into ASS(Sub Station Alpha V4) subtitles file

positional arguments:
  File or videoId       The file to be converted

optional arguments:
  -h, --help            show this help message and exit
  -l, --use-libass      fixes for libass
  -x 100, --reset-resolution-x 100
                        reset resolution X
  -y 100, --reset-resolution-y 100
                        reset resolution Y
  -f Microsoft YaHei UI, --font Microsoft YaHei UI 
                        specify font
  -d, --download-for-archive
                        Try downloading the annotations file from Internet Archive
  -i invidious-instances.domain, --invidious-domain invidious-instances.domain
                        Specify invidious instances
  -p, --preview-video   preview video, need mpv and specify invidious domain
  -g, --generate-video  generate video, need FFmpeg specify invidious domain

```

Example:

[Before](https://www.youtube.com/watch?v=HqSzHYxVKws)

```bash
Annotations2Sub.py -g HqSzHYxVKws
```

[After](https://www.bilibili.com/video/BV1Ff4y1t7Dj)

---
