#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "0.1.36"

"""
Annotations2Sub, 一个能把 Youtube 注释转换成 Sub Station Alpha V4 字幕文件的脚本

                                            xml.
                                            etree.
┌────────────────┐            ┌────────┐    ElementTree.  ┌─────────┐
│                │    read()  │        │    fromstring()  │         │     Parse()
│ Annotation.xml │ ─────────► │ String │ ───────────────► │ Element │ ────────────┐
│                │            │        │                  │         │             │
└────────────────┘            └────────┘                  └─────────┘             │
                                                                                  ▼
                                                                         ┌──────────────────┐
                                                                         │                  │
                                                                         │ List[Annotation] │
                                                                         │                  │
                                                                         └──────────────────┘

┌────────────────┐            ┌────────┐  Sub.      ┌─────────────┐               │
│                │  finally   │        │  Dump()    │             │  Convert()    │
│ Annotation.ass │ ◄───────── │ String │ ◄───────── │ List[Event] │ ◄─────────────┘
│                │            │        │            │             │
└────────────────┘            └────────┘            └─────────────┘

在 2019 年的某一天, 我在 Youtube 听歌, 发现字幕没了.
从评论区我得知: "從 2019 年 1 月 15 日起，我們將不再對觀眾顯示現有的註解。所有的現有註解都將移除。"
我当即破口大骂谷歌.
但我直觉告诉我应该有人存档,
还真的有! 鸣谢: https://archive.org/details/youtubeannotations
我想将其转换为我熟悉的 Sub Station Alpha 字幕, 我在搜索引擎查找我需要的东西, 
找到了 https://github.com/nirbheek/youtube-ass (致谢)
但是他并不好用, 压根就没法用
我改呀改, 这时我其实并不会编程, 但是我会谷歌, 让他可以运行也算是没有花费太长的时间.
但是效果并不能让人满意, 没有颜色, 只有字幕, 很不满意
于是我仔细阅读了他的源码, 发现实现很恶心, 竟然用样式来实现定位, 而且并不是 Sub Station Alpha 目前的事实标准(Aegisub)
但是拜其所致我脑内有了大概的思路, 于是我觉得把他砸了重写一个 :-)
回过头来, 这个过程让我学会了编程.

此项目早期(8e2d8eb 第一个勉强可用的版本)参照 https://github.com/nirbheek/youtube-ass 实现了一个简单的转换器, 
参照 https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范 实现了一个简单的 Sub Station Alpha 格式生成器
使用 "样式覆写代码" 实现了定位和颜色
之后(a64995 庆祝一下), 使用了 "绘图模式" 实现了 "popup" 样式
在 https://invidious.io/ 和 FFmpeg 的帮助下, 实现了简单的视频预览
再之后, 脚本逐步完善, 完成了 https://www.bilibili.com/video/BV1Ff4y1t7Dj
但是还是有些遗憾
---以下是有类似问题的视频，以制表符分隔---
videoId	title
g-0i6MOh7n0	志方あきこ - ラ・シェール 中文字幕(Chinese Translation)
aaLI3ErnHQg	志方あきこ - EXEC_HARMONIUS/. 中文字幕(Chinese Translation)
sgeXEwVWnpI	志方あきこ - EXEC_over.METHOD_SUBLIMATION/. ~omness chs ciel sos infel  中文字幕(Chinese Translation)
R4CqsDTnT60	志方あきこ - Ec Tisia ～Tarifa～ 中文字幕(Chinese Translation)
---以上是有类似问题的视频，以制表符分隔---
说实话我不想实现恶心的 CSS 定位

---

作为我的第一个代码, 我一直想让其趋于完美.
首先想的是参考 https://github.com/isaackd/annotationlib (致谢), 将 Annotation 抽成一个简单的结构, 
与脚本生成器(转换器)解耦, 结果并没有让事情变简单. (这是两年前的事了)
之后还尝试过实现 speech 样式, 把事情弄得一团糟
尝试过扔掉 invidious , 发现我简直像个shaberhu (这是一年前的事)
只好作罢, 上学去了.
...
自从 2022 年新年开始我已经半年呆在家里了, 我有了时间一直折腾代码, 我决定再次挑战这个目标.
首先, 我把我按照写 Go 的经验把脚本拆成了模块, 上传到了 PyPI, 并尝试为其编写单元测试, 并借以此实现了多语言
然后, 再次尝试将 Annotation 抽成一个简单的结构
现在, 我尝试对其进行详尽的注释, 到目前为止看起来不错.

---

"""
version = __version__
