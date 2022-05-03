# Annotations2Sub

一个可以把 Youtube 注释转换成 ASS(Sub Station Alpha V4) 字幕文件的脚本

A script that can convert Youtube Annotation into ASS(Sub Station Alpha V4) subtitles files

---

```man
usage: Annotations2Sub.py [-h] [-l] [-x 100] [-y 100] [-f Microsoft YaHei UI] [-d] [-i invidious.domain] [-p] [-g] 
                          File or videoId [File or videoId ...]

A script that converts Youtube Annotations into ASS(Sub Station Alpha V4) subtitles file

positional arguments:
  File or videoId       The file to be converted

optional arguments:
  -h, --help            show this help message and exit
  -l, --use-libass      Fixes for libass
  -x 100, --reset-resolution-x 100
                        Reset resolution X
  -y 100, --reset-resolution-y 100
                        Reset resolution Y
  -f Microsoft YaHei UI, --font Microsoft YaHei UI 
                        Specify font
  -d, --download-for-archive
                        Try downloading the annotations file from Internet Archive
  -i invidious.domain, --invidious-domain invidious.domain
                        Specify invidious domain
  -p, --preview-video   Preview video(need mpv)
  -g, --generate-video  Generate video (need FFmpeg)

```

---

Example:

```bash
wget https://github.com/USED255/Annotations2Sub/raw/master/Annotations2Sub.py 
```

[Before](https://www.youtube.com/watch?v=HqSzHYxVKws)

```bash
python .\Annotations2Sub.py -g HqSzHYxVKws
```

[After](https://www.bilibili.com/video/BV1Ff4y1t7Dj)

---
