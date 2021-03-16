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
  -p, --preview-video   Preview video(need mpv)
  -g, --generate-video  Generate video (need FFmpeg)

```

---

Example:

```
python .\Annotations2Sub.py -g e8kKeUuytqA
```

[Output](https://www.bilibili.com/video/BV1Ff4y1t7Dj?p=4)

---

[试例](https://www.used255.xyz/uploads/Annotations2Sub_试例)

---

## 失败的重构分支 

本次重构没有让编程更美好

## Failed refactoring branch 

This refactoring did not make programming better 