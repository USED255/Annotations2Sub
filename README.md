# Annotations2Sub

一个可以把 Youtube 注释转换成 ASS 字幕文件的脚本

A script that can convert Youtube Annotation into .ASS subtitles files

---

```man
usage: Annotations2Sub.py [-h] [-l] [-x 1920] [-y 1080] [-d] [-i invidious.domain] [-p] [-g] File or ID [File or ID ...]

A script that converts Youtube Annotations into .ASS subtitles

positional arguments:
  File or ID            The file to be converted

optional arguments:
  -h, --help            show this help message and exit
  -l, --use-libass      Fixes for libass
  -x 100, --reset-resolution-x 100
                        Reset resolution X
  -y 100, --reset-resolution-y 100
                        Reset resolution Y
  -f, --font            Specify font 
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
python3 .\Annotations2Sub.py -g e8kKeUuytqA
```

[After](https://www.bilibili.com/video/BV1Ff4y1t7Dj?p=4)

---

<details>
  <summary><mark><font color=darkred>TODO</font></mark></summary>

- g-0i6MOh7n0

- 29-q7YnyUmY

- 去除 invidious

</details>
