#

## 快速背景

本仓库用于将旧版 YouTube 注释 XML 文件转换为字幕格式(ASS/SSA). 包的入口点是控制台脚本 `Annotations2Sub`(在 `pyproject.toml` -> `project.scripts` 中定义). 主要代码位于 `src/Annotations2Sub/`, 测试代码位于 `src/tests/`.

## 总览

- 目的: 读取 YouTube 注释 XML 并生成字幕文件(ASS/SSA). 用户用法见 `README.md`: `Annotations2Sub <file.xml>`.
- 核心模块.
  - `src/Annotations2Sub/convert.py` —— 主要的转换逻辑和数据变换.
  - `src/Annotations2Sub/Annotations.py` —— XML 解析和注释数据结构.
  - `src/Annotations2Sub/subtitles/` —— 字幕格式、样式、事件和绘图辅助.
  - `src/Annotations2Sub/_main.py` / `src/Annotations2Sub/__main__.py` —— CLI 入口和主程序.

## 结构设计

- 关注点分离: 解析(`Annotations.py`)、转换(`convert.py`)、输出格式化(`subtitles/*`). 测试通过 `src/tests/testCase/Baseline/` 下的基线 `.test` 文件进行.

## 如何运行、测试和代码检查

- 推荐使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理和运行.

  `uv venv`

  `uv sync`

- 用示例文件运行 CLI.

  `Annotations2Sub src/tests/testCase/Baseline/annotations.xml.test`

- 运行单元测试(CI 使用 pytest).

  `pytest --cov=./ --cov-report=html`

- 代码检查与格式化.

  `mypy .`

  `isort .`

  `black .`

- CI 说明: GitHub Actions 工作流位于 `.github/workflows/`, 使用 `pytest --cov`, mypy 和 black 检查. 测试用例放在 `src/tests/`.

## 项目特有的模式和约定

- 测试用例使用 `src/tests/testCase/` 下的 `.test` 文件作为输入, 同时包含以 `.ass.test`、`.transform.ass.test` 等后缀的期望输出文件——添加转换测试时优先在此处添加新用例.
- 包通过 `py.typed`(见 `src/Annotations2Sub/py.typed`)暴露类型存根, 建议添加类型注解并保持 mypy 检查通过(CI 会运行 mypy).
- 本地化: gettext `.po`/`.mo` 文件在 `src/Annotations2Sub/locales/`. 如有用户可见字符串变更, 请更新 `.po` 文件并重新生成 `.mo`.

## 常见代码位置(便于修改时查阅)

- CLI 入口: `src/Annotations2Sub/_main.py`、`src/Annotations2Sub/__main__.py`
- 解析: `src/Annotations2Sub/Annotations.py`
- 转换流程: `src/Annotations2Sub/convert.py`
- 字幕格式实现: `src/Annotations2Sub/subtitles/*.py`
- 工具类: `src/Annotations2Sub/utils.py`、`cli_utils.py`
- 测试与用例: `src/tests/`, 尤其是 `src/tests/testCase/Baseline/`

## 集成点与外部依赖

- 无外部依赖.
- 构建/打包使用 setuptools(见 `pyproject.toml`).
- CI 会上传覆盖率到 Codecov；CI 测试会安装 pytest 并运行覆盖率.

## 问题咨询

- 在 GitHub 提 [issue](https://github.com/USED255/Annotations2Sub/issues).
