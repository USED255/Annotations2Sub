# Annotations2Sub Source Code

## 概述

Annotations2Sub 是一个将旧版 YouTube Annotations 的 XML 文件转换为 ASS 字幕文件的命令行工具. 入口点是控制台脚本 `Annotations2Sub`. 主要代码位于 `src/Annotations2Sub/`, 测试代码位于 `src/tests/`.

## 技术栈

- Python 3.7+
- 无外部依赖
- 使用 [uv](https://github.com/astral-sh/uv) 管理工具链, 使用 setuptools 打包, pytest 测试, mypy 类型检查, isort 和 black 进行代码格式化.

## 架构

- 流程: 解析(`Annotations.py`)、转换(`convert.py`)和输出(`subtitles/*`).
- 入口: `src/Annotations2Sub/_main.py` 或 `src/Annotations2Sub/__main__.py`.
- 核心模块:
  - `src/Annotations2Sub/Annotations.py` : XML 解析和Annotations数据结构.
  - `src/Annotations2Sub/convert.py` : 主要转换逻辑.
  - `src/Annotations2Sub/subtitles/` : 字幕格式、样式、事件和绘图辅助.
  - `src/Annotations2Sub/cli.py` : 用户界面.
- 测试:
  - `src/tests/test_Baseline.py` : 回归测试.
  - `src/tests/test_cli.py` : 集成测试.
  - `src/tests/unittest/` : 其他测试.

## 项目特有的模式

- 测试用例是 Youtube Annotations, 使用 `src/tests/testCase/` 下的 `.test` 文件作为输入, 同时包含以 `.ass.test`、`.transform.ass.test` 等后缀的期望输出文件.
- gettext `.po`/`.mo` 文件在 `src/Annotations2Sub/locales/`. 如有用户可见字符串变更, 请更新 `.po` 文件并重新生成 `.mo`.

## 如何运行、测试和代码检查

- 使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理.

  `uv sync`

- 之后激活你的虚拟环境.

- 用示例文件运行 CLI:

  `Annotations2Sub src/tests/testCase/Baseline/annotations.xml.test`

- 运行测试:

  `pytest --cov=./ --cov-report=html`

- 代码检查与格式化.

  `mypy .`

  `isort .`

  `black .`

## 调试 Annotations 行为

使用[youtube_annotations_hack](https://github.com/USED255/youtube_annotations_hack)来预览正确的注释行为.

## 工作流

项目协作使用 [GitHub 流程](https://docs.github.com/zh/get-started/using-github/github-flow).

## 问题咨询

请在 GitHub 提 [issue](https://github.com/USED255/Annotations2Sub/issues).

## 您也可以看看

- https://www.reddit.com/r/DataHoarder/comments/al7exa/youtube_annotation_archive_update_and_preview/

  可能是目前仅存的 Youtube Annotations.

- https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范

  整理好的关于 ASS 字幕文件的格式以及渲染行为的文档.

- https://github.com/USED255/youtube_annotations_hack

  衍生项目, 从 archive.org 拿到了旧版 Youtube 网页经过修改后可以在本地运行, 之后用 LLM 反混淆. 可以正确的重现 Youtube Annotations, 同时进行调试.
