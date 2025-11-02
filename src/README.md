# Annotations2Sub Source Code

## 快速背景

本仓库是一个用于将旧版 YouTube Annotations 的 XML 文件转换为 ASS 字幕文件的命令行工具. 包的入口点是控制台脚本 `Annotations2Sub`(在 `pyproject.toml` -> `project.scripts` 中定义). 主要代码位于 `src/Annotations2Sub/`, 测试代码位于 `src/tests/`.

## 组织结构

- 目的: 读取 YouTube Annotations XML 文件并生成 ASS 字幕文件. 用户用法见 `README.md`: `Annotations2Sub <file.xml>`.
- 流程: 解析(`Annotations.py`)、转换(`convert.py`)、输出(`subtitles/*`).
- 核心模块:
  - `src/Annotations2Sub/_main.py` 或 `src/Annotations2Sub/__main__.py` —— 程序入口.
  - `src/Annotations2Sub/Annotations.py` —— XML 解析和Annotations数据结构.
  - `src/Annotations2Sub/convert.py` —— 主要的转换逻辑和数据变换.
  - `src/Annotations2Sub/subtitles/` —— 字幕格式、样式、事件和绘图辅助.

## 如何运行、测试和代码检查

- 推荐使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理和运行.

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

## 项目特有的模式和约定

- 测试用例是 Youtube Annotations, 使用 `src/tests/testCase/` 下的 `.test` 文件作为输入, 同时包含以 `.ass.test`、`.transform.ass.test` 等后缀的期望输出文件.
- 添加类型注解并保持 mypy 检查通过.
- 使用 isort 和 black 进行代码格式化.
- 本地化: gettext `.po`/`.mo` 文件在 `src/Annotations2Sub/locales/`. 如有用户可见字符串变更, 请更新 `.po` 文件并重新生成 `.mo`.

## 集成点与外部依赖

- 无外部依赖.
- 构建/打包使用 setuptools.
- CI 会上传覆盖率到 Codecov.

## [TODO]

使用[youtube_annotations_hack](https://github.com/USED255/youtube_annotations_hack)来预览正确的注释行为[TODO]

## 工作流[TODO]

[TODO]

## 问题咨询

- 在 GitHub 提 [issue](https://github.com/USED255/Annotations2Sub/issues).

## 您也可以看看

- https://www.reddit.com/r/DataHoarder/comments/al7exa/youtube_annotation_archive_update_and_preview/

  可能是目前仅存的 Youtube Annotations.

- https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范

  整理过的关于 ASS 字幕文件的格式以及渲染行为的文档.

- https://github.com/USED255/youtube_annotations_hack

  衍生项目, 从 archive.org 拿到了旧版 Youtube 网页经过修改后可以在本地运行, 之后用 LLM 反混淆. 可以正确的重现 Youtube Annotations, 同时进行调试.
