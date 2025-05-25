# 简介

Annotations2Sub 是一个用于下载和转换 YouTube 注释的工具。由于 YouTube 已经移除了注释功能，该工具提供了一种保留和访问这些内容的方法。

其主要目的是获取注释文件（XML 格式）并将其转换为字幕格式。

主要功能包括：
* 从 YouTube（如果可用）或互联网档案馆下载注释文件。
* 将注释 XML 文件转换为字幕格式。
* 可指定视频分辨率进行转换。
* 可指定字幕字体。
* 支持使用 `mpv` 预览生成的带字幕的视频。
* 支持使用 `FFmpeg` 生成嵌入字幕的视频。
* 支持使用 Invidious 实例获取注释数据。

## 命令行界面 (CLI)

Annotations2Sub 主要通过其命令行界面使用。

### 命令格式

```
usage: Annotations2Sub.py [-h] [-l] [-x 100] [-y 100] [-f Arial ] [-o Folder] [-d]
                          [-i invidious.domain] [-p] [-g] [-s] [-n] [-k] [-u] [-v]
                          [-V]
                          文件或视频ID [文件或视频ID ...]
```

### 位置参数

*   `File or videoId (文件或视频ID)`: 指定要处理的本地注释 XML 文件的文件路径或 YouTube 视频 ID。可以提供多个文件或视频 ID。

### 可选参数

*   `-h, --help`: 显示帮助信息并退出。
*   `-x 100, --transform-resolution-x 100`: 转换分辨率 X。设置输出的水平分辨率。默认为 100。
*   `-y 100, --transform-resolution-y 100`: 转换分辨率 Y。设置输出的垂直分辨率。默认为 100。
*   `-f Arial, --font Arial`: 指定字幕所用字体。默认为 "Arial"。
*   `-d, --download-for-archive`: 尝试从互联网档案馆下载注释文件。
*   `-D, --download-annotations-only`: 仅下载注释文件。不执行转换操作。
*   `-p, --preview-video`: 使用生成的字幕预览视频。需要安装 `mpv` (https://mpv.io/)。
*   `-g, --generate-video`: 生成嵌入字幕的视频。需要安装 `FFmpeg` (https://ffmpeg.org/)。
*   `-i invidious-instances.domain, --invidious-instances invidious-instances.domain`: 指定用于下载的 Invidious 实例 (例如 `invidious.snopyta.org`)。实例列表请参阅 https://redirect.invidious.io/。
*   `-n, --no-overwrite-files`: 不覆盖现有文件。如果输出文件已存在，则工具不会写入该文件。
*   `-N, --no-keep-intermediate-files`: 不保留处理过程中生成的中间文件（例如，如果同时进行了转换，则不保留下载的 XML 文件）。
*   `-O directory, --output-directory directory`: 指定转换后文件的输出目录。
*   `-o File, --output File`: 指定输出文件名。如果为 "-"，则输出到标准输出。通常在处理单个输入时使用。
*   `-v, --version`: 显示程序版本号并退出。
*   `-V, --verbose`: 在处理过程中显示更详细的信息。

### 使用示例

1.  **转换本地注释文件:**
    ```bash
    Annotations2Sub 29-q7YnyUmY.xml
    ```

2.  **下载并转换 YouTube 视频的注释:**
    （如果同时指定了 `-d`，将首先尝试从 YouTube 下载，然后从互联网档案馆下载）
    ```bash
    Annotations2Sub 29-q7YnyUmY
    ```

3.  **从互联网档案馆下载 YouTube 视频的注释并转换:**
    ```bash
    Annotations2Sub -d 29-q7YnyUmY
    ```

4.  **生成带内嵌字幕的视频:**
    ```bash
    Annotations2Sub -g 29-q7YnyUmY
    ```

5.  **使用特定的 Invidious 实例下载注释并保存到指定输出目录:**
    ```bash
    Annotations2Sub -i invidious.snopyta.org -O ./my_annotations 29-q7YnyUmY
    ```

6.  **转换本地文件，同时指定输出分辨率和字体:**
    ```bash
    Annotations2Sub -x 1920 -y 1080 -f "宋体" my_video_annotations.xml
    ```

## 核心功能与工作流程

Annotations2Sub 处理 YouTube 注释文件 (通常是 `annotations.xml`) 并将其转换为字幕格式，如 Advanced SubStation Alpha (`.ass`)。其大致工作流程如下：

1.  **输入 (Input)**:
    *   主要输入是一个包含 YouTube 注释数据的 XML 文件 (`Annotations.xml`)。
    *   此文件可以是本地文件，也可以通过视频 ID 下载。该工具可以直接从 YouTube 获取 (如果该视频的注释仍然可用)，或者从互联网档案馆 (Internet Archive) 或通过 Invidious 实例等存档中获取。

2.  **解析 (Parsing)**:
    *   从文件或下载流中读取的原始 XML 数据会使用 Python 的 `xml.etree.ElementTree.fromstring()` 函数进行解析。这将 XML 字符串转换为一个 `Element` 对象，这是一个树状的 XML 结构表示。
    *   然后，此 `Element` 对象由一个自定义的 `Parse()` 函数处理。该函数遍历 XML 树，提取相关的注释数据 (文本、时间、位置、样式等)，并将其转换为结构化的 `Annotation` 对象列表 (`List[Annotation]`)。每个 `Annotation` 对象代表原始 YouTube 注释中的单个注释事件或元素。

3.  **转换 (Conversion)**:
    *   从解析步骤中获得的 `List[Annotation]` 会被传递给一个 `Convert()` 函数。
    *   该函数接收结构化的注释数据，并将其转换为字幕 `Event` 对象列表 (`List[Event]`)。一个 `Event` 通常代表输出字幕文件中的单行或文本块，及其关联的时间 (开始和结束) 和样式信息。
    *   在此阶段，来自注释的样式信息 (如位置、颜色、字体大小，这些是原始 YouTube 注释系统的一部分) 会被转换为目标字幕格式的等效样式指令 (例如 ASS 标签)。

4.  **输出生成 (Output Generation)**:
    *   `List[Event]` 以及任何必要的头部信息和样式定义 (通常封装在一个 `Sub` 对象中，该对象也可能包含 `Style` 对象)，然后被格式化为符合所选字幕文件格式的字符串。
    *   最常见的输出格式是 `.ass` (Advanced SubStation Alpha)，它支持丰富的样式和定位。
    *   最终的字符串随后被写入输出文件 (例如 `video_annotations.ass`) 或标准输出。

该过程可以大致描述为：

```
[Annotations.xml 文件] --(读取文件)--> [XML 字符串] --(xml.etree.ElementTree.fromstring())--> [Element 对象]
                                                                                                   |
                                                                                                   | Parse()
                                                                                                   ▼
                                                                                         [Annotation 对象列表]
                                                                                                   |
                                                                                                   | Convert()
                                                                                                   ▼
                                                                                         [Event 对象列表 (字幕事件)]
                                                                                                   |
                                                                                                   | (str(Sub) / 格式化为字符串)
                                                                                                   ▼
                                                                                         [输出字符串 (例如 .ass 格式)] --(写入文件)--> [Annotations.ass 文件]
```

### 附加功能

除了这个核心转换工作流程之外，Annotations2Sub 还提供了几个相关功能，通常通过命令行选项访问：

*   **视频预览 (Video Preview)**: 使用 `mpv`，该工具可以显示视频以及生成的字幕，以便立即预览。
*   **视频生成 (Video Generation)**: 使用 `FFmpeg`，Annotations2Sub 可以创建一个新的视频文件，并将字幕硬编码 (嵌入) 到视频帧上。
*   **下载 (Downloading)**: 如前所述，它包括了强大的下载注释文件选项，包括从互联网档案馆和 Invidious 实例下载，这至关重要，因为 YouTube 已移除了对注释的直接访问。

## 依赖与安装

### 主要工具安装

Annotations2Sub 是一个 Python 包，可以使用 `pip` 轻松安装：

```bash
pip install Annotations2Sub
```

此命令将从 Python 包索引 (PyPI) 下载 Annotations2Sub 并安装它及其 Python 依赖项。

### 外部依赖

对于某些功能，Annotations2Sub 依赖于需要单独安装在您系统上的外部命令行工具：

*   **FFmpeg** (`https://ffmpeg.org/`):
    *   **用途**: 视频生成功能 (`-g` 或 `--generate-video` 选项) 需要。FFmpeg 用于获取输入视频并将转换后的注释作为硬编码字幕嵌入到新的视频文件中。
    *   **安装**: 从 FFmpeg 网站下载并根据您的操作系统说明进行安装。确保将其添加到系统的 PATH 中，以便 `Annotations2Sub` 可以调用它。

*   **mpv** (`https://mpv.io/`):
    *   **用途**: 视频预览功能 (`-p` 或 `--preview-video` 选项) 需要。`mpv` 是一个媒体播放器，用于播放原始视频及生成的字幕文件，以便快速检查。
    *   **安装**: 从 mpv 网站下载并安装。确保它在您系统的 PATH 中可用。

如果您不需要视频生成或预览功能，则无需安装 FFmpeg 或 mpv。核心的注释下载和转换功能仍然可以工作。

## 项目历史与动机

Annotations2Sub 的诞生直接回应了 YouTube 在 2019 年 1 月决定停止注释功能的事件。该项目的作者是一位 YouTube 的忠实用户，他发现对于像音乐视频中的翻译字幕这类内容至关重要的注释功能正在消失。这激发了他保存这种独特内容形式的强烈愿望。

**最初的火花与学习曲线:**
当了解到互联网档案馆 (Internet Archive) 等实体已存档了注释数据后，作者开始寻找工具将这些 XML 文件转换为可用的字幕格式 (如 Advanced SubStation Alpha - ASS)。现有的工具，例如 `youtube-ass`，被发现存在不足，缺乏颜色和精确定位等功能，或者根本难以使用。

尽管当时没有编程背景，但作者决心创建一个更好的解决方案。这标志着他编程学习之旅的开始，最初的目标是使存档的注释变得可用。

**开发里程碑:**
*   **早期版本:** 最初可用的版本受到 `youtube-ass` 和基本的 ASS 格式规范的启发。采用了诸如“样式覆盖代码”之类的技术来处理注释的定位和颜色。
*   **功能增强:** 使用“绘图模式”添加了对“弹出式”样式注释的支持。与 Invidious (用于获取注释数据) 以及 FFmpeg/mpv (用于视频生成和预览) 的集成，极大地扩展了该工具的功能。
*   **克服挑战:** 开发过程并非一帆风顺。准确复制 YouTube 注释中复杂的类似 CSS 的定位功能被证明是困难的。为了获得更好的模块化而进行的重构代码的尝试 (例如，受 `annotationlib` 启发，将解析与生成分离) 是迭代优化过程的一部分。
*   **重新聚焦 (2022年):** 一段时期的集中开发工作使得代码结构得到了显著改进，包括模块化、添加单元测试、类型检查以及通过详细注释全面提升代码质量。
*   **利用存档:** 在互联网档案馆上发现的旧 YouTube 网页存档为调试和理解注释的正确视觉表现提供了宝贵的资源。此外，将来自 `archive.omar.yt` 的大型 Zstandard 压缩的 YouTube 注释压缩包处理成 SQLite 数据库，增强了该工具处理各种注释文件的稳健性。

这个项目源于保存一种正在消失的互联网功能的个人需求，最终演变成一个功能全面的工具，作者也在此过程中学会了编程。它证明了人们对存档和维护数字遗产的渴望。

## 故障排除与已知问题

### 一般免责声明

**重要提示：** 正如项目 `README.md` 中所述：
> 因为字幕滤镜的行为和怪癖不断变动, 以及 Web 技术和字幕技术上的巨大差异, 本项目无法正确还原注释的行为。

尽管 Annotations2Sub 尽力尽可能准确地转换 YouTube 注释，但用户应意识到，完美 1:1 复制原始浏览器渲染通常是无法实现的。这是由于：
*   Web 浏览器渲染内容 (HTML, CSS, JavaScript) 的方式与字幕格式 (如 ASS) 显示文本和图形的方式之间存在根本差异。
*   YouTube 原始注释系统的复杂性以及有时不一致的行为。
*   不同视频播放器解释字幕样式的方式存在差异。

### 常见问题与解决方案

1.  **视频生成/预览无法工作:**
    *   **问题:** `-g` (生成视频) 或 `-p` (预览视频) 选项产生错误或无法工作。
    *   **解决方案:** 确保 **FFmpeg** (用于 `-g`) 和/或 **mpv** (用于 `-p`) 已在您的系统上正确安装，并且至关重要的是，它们的可执行文件位置已包含在您系统的 `PATH` 环境变量中。有关更多详细信息，请参阅“依赖与安装”部分。

2.  **字体相关问题:**
    *   **问题:** 字幕显示字体不正确，或特殊字符无法正确显示。
    *   **解决方案:**
        *   默认使用的字体是 "Arial"。如果您的系统上没有此字体，将使用备用字体，这可能会改变外观。您可以使用 `-f` 或 `--font` 命令行选项指定不同的字体 (例如 `-f "SimSun"` 来使用宋体)。
        *   确保所选字体支持注释语言所需的所有字符。对于某些语言或特殊符号，可能需要更全面的字体。
        *   字体的处理方式也可能取决于您使用的视频播放器的字幕渲染引擎。

3.  **特定注释文件的问题:**
    *   **问题:**某个特定的 `annotations.xml` 文件转换失败或产生乱码输出。
    *   **解决方案:** 虽然该工具已经使用包括来自存档的大型数据库在内的各种注释文件进行了测试，但一些非常旧的、结构独特的或可能已损坏的注释 XML 文件可能无法完美处理。如果您遇到此类文件，可以考虑在项目的代码仓库中报告为问题，并在可能的情况下提供有问题的 XML 文件。

4.  **Invidious 实例问题:**
    *   **问题:** 通过 Invidious 实例 (`-i` 选项) 下载注释失败。
    *   **解决方案:** Invidious 实例由社区托管，其可用性可能会发生变化。如果一个实例不起作用，请尝试公共列表 (例如 https://redirect.invidious.io/) 中的其他实例。某些实例可能会比较慢或过载。

5.  **不正确的视觉表现:**
    *   **问题:** 字幕输出中注释的位置、大小或样式与它们在 YouTube 上的显示不完全匹配。
    *   **解决方案:** 这与一般免责声明有关。转换过程涉及将基于 Web 的渲染逻辑转换为字幕系统逻辑，这可能导致差异。该工具会尝试进行最大努力的转换。调整分辨率参数 (`-x`, `-y`) 有时可能有助于解决缩放问题，但复杂的交互式或重度样式的注释尤其难以完美复制。

如果您遇到持续存在的问题，检查程序的输出以获取错误消息 (使用 `-V` 或 `--verbose` 选项获取更多详细信息) 可以提供线索。

## 贡献

我们非常欢迎对 Annotations2Sub 项目的贡献！无论您有建议、报告错误，还是希望贡献代码，我们都非常感谢您的帮助。

请访问项目的 [GitHub 页面](https://github.com/USED255/Annotations2Sub) 获取更多信息。在那里您可以：
*   查看现有问题或报告新问题。
*   建议新功能或改进。
*   提交包含您贡献的拉取请求 (Pull Request)。

如果您计划贡献代码，建议您首先通过“问题 (Issue)”就您提议的更改进行讨论，特别是对于较大的贡献。

## 许可证

Annotations2Sub 根据 [GPLv3 许可证](https://www.gnu.org/licenses/gpl-3.0.zh-cn.html) 授权。
