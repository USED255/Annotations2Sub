# Annotations2Sub

将 YouTube 注释转换为字幕.

[![License GPLv3](https://img.shields.io/pypi/l/Annotations2Sub?color=1)](https://pypi.org/project/Annotations2Sub/)
[![Test](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml/badge.svg)](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/USED255/Annotations2Sub/branch/master/graph/badge.svg?token=SSNQNEAXMP)](https://codecov.io/gh/USED255/Annotations2Sub)
[![Version](https://img.shields.io/pypi/v/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)
[![Python version](https://img.shields.io/pypi/pyversions/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)

---

在开始之前, 请准备好 Python, YouTube 注释的 XML 文件, 视频播放器, 视频文件, 以及其相关背景知识.

安装:

```bash
pip install Annotations2Sub
```

转换注释:

```bash
Annotations2Sub XXXXXXXXXXX.xml
```

之后使用视频播放器播放视频并挂载输出的字幕文件.

---

YouTube 注释是 YouTube 于 2008 年推出的一项功能, 允许视频创作者在视频中添加文本、链接和互动元素, 以增强观看体验. YouTube 于 2019 年移除了此功能.

ASS 字幕是一种常见的外挂字幕格式, 全称 Advanced SubStation Alpha. 与其他字幕格式相比, 他能够设置字体、颜色、位置, 甚至添加图像和特效, 增强您的观看体验.

此工具可以帮助您将 YouTube 注释转换为 ASS 字幕文件, 您可以播放或添加到视频中. 如果您不需要此功能, 建议使用 [AnnotationsRestored](https://github.com/isaackd/AnnotationsRestored).

---

致谢:
[omarroth](https://www.reddit.com/r/DataHoarder/comments/al7exa/youtube_annotation_archive_update_and_preview/),
[Nirbheek Chauhan](https://github.com/nirbheek/youtube-ass),
[Zhenye Wei](https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范),
[Invidious](https://invidious.io/),
[Isaac](https://github.com/isaackd/annotationlib),
[Eva](https://github.com/po5/assnotations),
[Internet Archive](https://archive.org/),
[Gemini 1.5 Pro](https://deepmind.google/models/gemini/pro/),
[Rain Shimotsuki](https://www.youtube.com/@rain_shimotsuki),
[KeksusGSPB](https://www.youtube.com/watch?v=c1iCjpxDxz4),
[XNX.ROmania](https://web.archive.org/web/20230227230532/https://www.youtube.com/watch?v=M2ryDEyyrXE).
