#

## 快速背景

本仓库用于将旧版 YouTube 注释 XML 文件转换为字幕格式(ASS/SSA). 包的入口点是控制台脚本 `Annotations2Sub`(在 `pyproject.toml` -> `project.scripts` 中定义). 主要代码位于 `src/Annotations2Sub/`, 测试代码位于 `src/tests/`.

## 组织结构

- 目的: 读取 YouTube 注释 XML 并生成字幕文件(ASS/SSA). 用户用法见 `README.md`: `Annotations2Sub <file.xml>`.
- 流程: 解析(`Annotations.py`)、转换(`convert.py`)、输出(`subtitles/*`).
- 测试通过 `src/tests/testCase/Baseline/` 下的基线 `.test` 文件进行.
- 核心模块:
  - `src/Annotations2Sub/convert.py` —— 主要的转换逻辑和数据变换.
  - `src/Annotations2Sub/Annotations.py` —— XML 解析和注释数据结构.
  - `src/Annotations2Sub/subtitles/` —— 字幕格式、样式、事件和绘图辅助.
  - `src/Annotations2Sub/_main.py` / `src/Annotations2Sub/__main__.py` —— CLI 入口和主程序

## 如何运行、测试和代码检查

- 推荐使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理和运行.

  `uv sync`

- 之后激活你的虚拟环境.

- 用示例文件运行 CLI.

  `Annotations2Sub src/tests/testCase/Baseline/annotations.xml.test`

- 运行单元测试(CI 使用 pytest).

  `pytest --cov=./ --cov-report=html`

- 代码检查与格式化.

  `mypy .`

  `isort .`

  `black .`

- CI 说明: GitHub Actions 工作流位于 `.github/workflows/`.

## 项目特有的模式和约定

- 测试用例使用 `src/tests/testCase/` 下的 `.test` 文件作为输入, 同时包含以 `.ass.test`、`.transform.ass.test` 等后缀的期望输出文件
- 建议添加类型注解并保持 mypy 检查通过(CI 会运行 mypy).
- 本地化: gettext `.po`/`.mo` 文件在 `src/Annotations2Sub/locales/`. 如有用户可见字符串变更, 请更新 `.po` 文件并重新生成 `.mo`.

## 集成点与外部依赖

- 无外部依赖.
- 构建/打包使用 setuptools(见 `pyproject.toml`).
- CI 会上传覆盖率到 Codecov；CI 测试会安装 pytest 并运行覆盖率, 尽可能覆盖所有代码.

## 问题咨询

- 在 GitHub 提 [issue](https://github.com/USED255/Annotations2Sub/issues).

## 您也可以看看

- https://www.reddit.com/r/DataHoarder/comments/al7exa/youtube_annotation_archive_update_and_preview/
- https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
- https://github.com/USED255/youtube_annotations_hack
