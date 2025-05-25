# -*- coding: utf-8 -*-
"""为应用程序提供一个简单的全局标志管理器。

此模块定义了一个 `flags` 类和一个全局实例 `Flags`，
可用于存储和访问全局应用程序设置或状态，例如详细级别。
"""


class flags:
    def __init__(self):
        self.verbose = False


Flags = flags()
