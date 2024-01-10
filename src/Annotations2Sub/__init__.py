#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Annotations2Sub, 一个能把 Youtube 注释转换成 Advanced SubStation Alpha 字幕文件的脚本"""

__version__ = "2.13.0"

"""
                                            xml.
                                            etree.
┌─────────────────┐            ┌────────┐    ElementTree.  ┌─────────┐
│                 │    read()  │        │    fromstring()  │         │     Parse()
│ Annotations.xml │ ─────────► │ String │ ───────────────► │ Element │ ────────────┐
│                 │            │        │                  │         │             │
└─────────────────┘            └────────┘                  └─────────┘             │
                                                                                  ▼
                                                                         ┌──────────────────┐
                                                                         │                  │
                                                                         │ List[Annotation] │
                                                                         │                  │
                                                                         └──────────────────┘

┌─────────────────┐            ┌────────┐  Sub.      ┌─────────────┐               │
│                 │  finally   │        │  Dump()    │             │  Convert()    │
│ Annotations.ass │ ◄───────── │ String │ ◄───────── │ List[Event] │ ◄─────────────┘
│                 │            │        │            │             │
└─────────────────┘            └────────┘            └─────────────┘

https://www.youtube.com/channel/UCe4QujtMby3h6dge1eYaPig
在 2019 年的某一天, 我在 Youtube 听歌, 发现字幕没了.
从评论区我得知: 「 從 2019 年 1 月 15 日起，我們將不再對觀眾顯示現有的註解。所有的現有註解都將移除。」
我当即破口大骂谷歌.
但我直觉告诉我应该有人存档,
还真的有! 鸣谢: https://archive.org/details/youtubeannotations
我尝试将其转换为我熟悉的 Advanced SubStation Alpha 字幕, 我在搜索引擎查找呀找, 
找到了 https://github.com/nirbheek/youtube-ass (致谢)
但是他并不是不好用, 是压根就没法用.
我改呀改, 但是我其实并不会编程, 但是我会谷歌, 让他可以运行也没有花费太长的时间
但是他并不让人满意, 没有颜色, 只有字幕, 很不爽.
我仔细阅读了他的源码, 发现实现很恶心, 竟然用样式来实现定位, 而且并不是目前的事实标准(Aegisub)
但是拜其所致我脑内有了大概的思路, 于是我决定砸了重写一个 :-)
回过头来, 这个过程让我学会了编程.

此项目早期(8e2d8eb 第一个勉强可用的版本)参照 https://github.com/nirbheek/youtube-ass 实现了一个简单的转换器, 
参照 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 实现了一个简单的 Advanced SubStation Alpha 生成器
使用 "样式覆写代码" 实现了定位和颜色
之后(a649956 庆祝一下), 使用 "绘图模式" 实现了 "popup" 样式
在 https://invidious.io/ 和 FFmpeg 的帮助下, 实现了简单的视频预览
之后, 脚本逐步完善, 完成了 https://www.bilibili.com/video/BV1Ff4y1t7Dj
但是还是有些遗憾
---以下是有类似问题的视频，以制表符分隔---
videoId	title
g-0i6MOh7n0	志方あきこ - ラ・シェール 中文字幕(Chinese Translation)
aaLI3ErnHQg	志方あきこ - EXEC_HARMONIUS/. 中文字幕(Chinese Translation)
sgeXEwVWnpI	志方あきこ - EXEC_over.METHOD_SUBLIMATION/. ~omness chs ciel sos infel  中文字幕(Chinese Translation)
R4CqsDTnT60	志方あきこ - Ec Tisia ～Tarifa～ 中文字幕(Chinese Translation)
---以上是有类似问题的视频，以制表符分隔---
说实话我不想实现恶心的 CSS 定位
更何况 annotationlib 都没有正确实现定位

---

作为我的第一个代码, 我一直想让其趋于完美.
首先想的是参考 https://github.com/isaackd/annotationlib (致谢), 将 Annotations 抽成一个简单的结构, 
与脚本生成器(转换器)解耦, 结果并没有让事情变简单. (2020)
之后还尝试过实现 speech 样式, 把事情弄得一团糟
还尝试过扔掉 invidious , 发现我简直像个shaberhu (2021)
只好作罢, 上学去了.
...
拜奥密克戎所赐自从 2022 年我已经有半年呆在家里了, 我有了时间可以一直折腾代码, 我决定再次挑战这个目标.
首先, 我依照写 Go 的经验将脚本拆成了模块, 编写单元测试, 进行类型检查, 一键格式化
然后, 尝试将 Annotations 抽成一个简单的结构
最后, 对其进行详尽的注释, 到目前为止看起来不错.
...
差不多完事儿了, 剩下的时间就是维护代码了.

---

没想到还有 https://github.com/po5/assnotations
...

---
- 注释(Annotations): YouTube 的功能
- SSA(Sub Station Alpha): 字幕格式
- ASS(Advanced SubStation Alpha): 字幕格式
- invidious(https://invidious.io/): 开源 YouTube 前端

"""
version = __version__

from Annotations2Sub.Annotations import Annotation, Parse
from Annotations2Sub.Convert import Convert
from Annotations2Sub.Sub import Sub

__all__ = ["Parse", "Annotation", "Convert", "Sub", "version"]
