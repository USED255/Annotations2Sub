#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

┌────────────────┐            ┌────────┐            ┌─────────────┐               │
│                │  finally   │        │  Dump()    │             │  Convert()    │
│ Annotation.ass │ ◄───────── │ String │ ◄───────── │ List[Event] │ ◄─────────────┘
│                │            │        │            │             │
└────────────────┘            └────────┘            └─────────────┘

在 2019 年的某一天, 我在 Youtube 听歌, 发现字幕没了.
从评论区我得知: "從 2019 年 1 月 15 日起，我們將不再對觀眾顯示現有的註解。所有的現有註解都將移除。"
我当即破口大骂谷歌.
但我直觉告诉我应该有人存档,
还真的有! 鸣谢: https://archive.org/details/youtubeannotations
我想将其转换为我熟悉的 Sub Station Alpha 字幕, 我在搜索引擎查找我需要的东西, 找到了 https://github.com/nirbheek/youtube-ass (致谢)
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
在之后, 脚本逐步完善, 完成了 https://www.bilibili.com/video/BV1Ff4y1t7Dj

"""


import argparse
import gettext
import xml.etree.ElementTree
from Annotations2Sub.Annotation import Parse

from Annotations2Sub.Convert import Convert
from Annotations2Sub.Sub import Sub

_ = gettext.gettext


def main():
    parser = argparse.ArgumentParser(description=_("一个可以把Youtube注释转换成ASS字幕的脚本"))
    parser.add_argument(
        "File", type=str, nargs="+", metavar="File or videoId", help=_("待转换的文件")
    )
    args = parser.parse_args()
    file = args.File[0]
    string = open(file, "r", encoding="utf-8").read()
    tree = xml.etree.ElementTree.fromstring(string)
    annotations = Parse(tree)
    events = Convert(annotations)
    sub = Sub()
    sub.events.events.extend(events)
    sub.info.info["PlayResX"] = 100
    sub.info.info["PlayResY"] = 100
    sub.events.events.sort(key=lambda event: event.Start)
    s = sub.Dump()
    with open(file + ".ass", "w", encoding="utf-8") as f:
        f.write(s)


if __name__ == "__main__":
    main()
