# Annotations2Sub

下载和转换 Youtube 注释

Download and convert Youtube Annotations

[![License GPLv3](https://img.shields.io/pypi/l/Annotations2Sub?color=1)](https://pypi.org/project/Annotations2Sub/)
[![Test](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml/badge.svg)](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/USED255/Annotations2Sub/branch/master/graph/badge.svg?token=SSNQNEAXMP)](https://codecov.io/gh/USED255/Annotations2Sub)
[![Version](https://img.shields.io/pypi/v/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)
[![Python version](https://img.shields.io/pypi/pyversions/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)

---

## The Problem / 问题说明

YouTube annotations were a popular feature that allowed creators to add interactive commentary, links, and other information directly into their videos. However, YouTube deprecated this feature in 2019, and all existing annotations were removed. This resulted in the loss of a significant amount of creative content and valuable information.

Annotations2Sub helps address this problem by providing a way to download and convert YouTube annotations into the ASS subtitle format. This allows you to preserve and view annotations even though they are no longer available on YouTube.

YouTube 注释曾是一项广受欢迎的功能，创作者可以通过它在视频中直接添加互动评论、链接和其他信息。然而，YouTube 于 2019 年弃用了此功能，并移除了所有现存的注释。这导致了大量创意内容和宝贵信息的丢失。

Annotations2Sub 通过提供下载 YouTube 注释并将其转换为 ASS 字幕格式的方法来帮助解决此问题。这使您即使在注释已从 YouTube 上移除的情况下，也能够保存和查看它们。

**因为字幕滤镜的行为和怪癖不断变动, 以及 Web 技术和字幕技术上的巨大差异, 本项目无法正确还原注释的行为**

**Because of the ever-changing behavior and quirks of subtitle filters, and the vast differences between web and subtitle technologies, this project was unable to correctly restore the behavior of annotations.**

```bash
pip install Annotations2Sub
```

```help
usage: Annotations2Sub.py [-h] [-l] [-x 100] [-y 100] [-f Arial ] [-o Folder] [-d]
                          [-i invidious.domain] [-p] [-g] [-s] [-n] [-k] [-u] [-v]
                          [-V]
                          File or videoId [File or videoId ...]

Download and convert Youtube Annotations

positional arguments:
  File or videoId       File path or video ID of multiple files to be convert

optional arguments:
  -h, --help            Show this help message and exit
  -x 100, --transform-resolution-x 100
                        Transform resolution X
  -y 100, --transform-resolution-y 100
                        Transform resolution Y
  -f Arial, --font Arial
                        Specify font
  -d, --download-for-archive
                        Try to download the Annotations file from Internet Archive
  -D, --download-annotations-only
                        Download Annotations only
  -p, --preview-video   Preview video, requires mpv(https://mpv.io/)
  -g, --generate-video  Generate video, requires FFmpeg(https://ffmpeg.org/)
  -i invidious-instances.domain, --invidious-instances invidious-instances.domain
                        Specify invidious instances (https://redirect.invidious.io/)
  -n, --no-overwrite-files
                        Do not overwrite files
  -N, --no-keep-intermediate-files
                        Do not keep intermediate files
  -O directory, --output-directory directory
                        Specify the output directory for the converted file
  -o File, --output File
                        Save to this file, if "-" then output to standard output
  -v, --version         Show version
  -V, --verbose         Show more messages
```

---

## Usage Examples / 用法示例

### Convert a local annotations file / 转换本地注释文件

If you have an annotations XML file saved locally, you can convert it to ASS format:
如果你在本地保存了注释 XML 文件，可以将其转换为 ASS 格式：

```bash
Annotations2Sub annotations.xml
```

### Download and convert annotations for a video ID / 下载并转换指定视频 ID 的注释

You can directly download and convert annotations for a given YouTube video ID:
你可以直接下载并转换给定 YouTube 视频 ID 的注释：

```bash
Annotations2Sub -d 29-q7YnyUmY
```

This will attempt to fetch the annotations from the Internet Archive.
此命令将尝试从互联网档案馆获取注释。

### Specify output directory / 指定输出目录

To save the converted ASS file to a specific directory:
要将转换后的 ASS 文件保存到特定目录：

```bash
Annotations2Sub -d 29-q7YnyUmY -O /path/to/output/directory/
```

### Specify output filename / 指定输出文件名

To save the converted ASS file with a specific name:
要将转换后的 ASS 文件以特定名称保存：

```bash
Annotations2Sub -d 29-q7YnyUmY -o my_video_annotations.ass
```

### Download annotations only / 仅下载注释

If you only want to download the raw annotation XML file without converting it:
如果你只想下载原始注释 XML 文件而不进行转换：

```bash
Annotations2Sub -D 29-q7YnyUmY
```

### Preview video with annotations (requires mpv) / 使用 mpv 预览带注释的视频 (需要 mpv)

To preview a video with the generated annotations using mpv:
要使用 mpv 预览带有所生成注释的视频：

```bash
Annotations2Sub -p 29-q7YnyUmY
```
This will download the annotations, convert them, and then launch mpv to play the video with the subtitles. You need to have the video file locally or provide a URL to the video.
此命令将下载注释，进行转换，然后启动 mpv 播放带字幕的视频。你需要本地拥有该视频文件，或者提供视频的 URL。

### Generate video with hardcoded annotations (requires FFmpeg) / 生成带硬编码注释的视频 (需要 FFmpeg)

To create a new video file with the annotations burned into the video (hardsubs):
要创建将注释嵌入视频（硬字幕）的新视频文件：

```bash
Annotations2Sub -g 29-q7YnyUmY
```
This also requires the original video to be available locally or via a URL. FFmpeg will be used to process the video.
这也需要原始视频在本地可用或通过 URL 提供。FFmpeg 将用于处理视频。

### Using a specific Invidious instance / 使用特定的 Invidious 实例

If you want to use a specific Invidious instance for fetching information (useful if the default is blocked or slow):
如果你想使用特定的 Invidious 实例来获取信息（在默认实例被屏蔽或速度较慢时很有用）：
```bash
Annotations2Sub -d 29-q7YnyUmY -i invidious.snopyta.org
```

### Adjusting resolution for conversion / 调整转换分辨率

Annotations are often tied to the resolution of the video they were created for. If the default (100x100) is not suitable, you can specify the target video resolution:
注释通常与其创建时所用视频的分辨率相关联。如果默认值 (100x100) 不适用，你可以指定目标视频分辨率：

```bash
Annotations2Sub -d 29-q7YnyUmY -x 1920 -y 1080
```
This helps in scaling the annotation elements correctly in the ASS file.
这有助于在 ASS 文件中正确缩放注释元素。

### Specifying font / 指定字体

You can specify a font to be used in the ASS file:
你可以在 ASS 文件中指定要使用的字体：
```bash
Annotations2Sub -d 29-q7YnyUmY -f "Comic Sans MS"
```
Make sure the font is available on the system where the subtitles will be viewed.
请确保在观看字幕的系统上该字体可用。

---

## Output Format: ASS Subtitles / 输出格式：ASS 字幕

Annotations2Sub converts YouTube annotations into the **Advanced SubStation Alpha (ASS)** subtitle format. ASS is a powerful subtitle format that allows for advanced features like:

*   **Styled text:** Control over font, size, color, bold, italics, etc.
*   **Positioning:** Precise placement of subtitles on the screen.
*   **Drawing commands:** Ability to draw vector shapes (used by Annotations2Sub to replicate annotation boxes and speech bubbles).
*   **Timing:** Accurate synchronization of subtitles with video frames.
*   **Layers:** Control over how overlapping subtitles are displayed.

Annotations2Sub 将 YouTube 注释转换为 **Advanced SubStation Alpha (ASS)** 字幕格式。ASS 是一种功能强大的字幕格式，支持以下高级功能：

*   **样式文本：** 控制字体、大小、颜色、粗体、斜体等。
*   **定位：** 在屏幕上精确定位字幕。
*   **绘图命令：** 能够绘制矢量图形（Annotations2Sub 用于复制注释框和气泡）。
*   **计时：** 字幕与视频帧的精确同步。
*   **图层：** 控制重叠字幕的显示方式。

ASS files are plain text files with a `.ass` extension. They can be played with most modern video players, such as VLC, mpv, MPC-HC, and PotPlayer. Many video players will automatically load ASS files if they have the same name as the video file and are in the same directory.

ASS 文件是带有 `.ass` 扩展名的纯文本文件。大多数现代视频播放器（如 VLC、mpv、MPC-HC 和 PotPlayer）都可以播放它们。如果 ASS 文件与视频文件同名且位于同一目录中，许多视频播放器会自动加载它们。

The use of ASS format allows Annotations2Sub to replicate the appearance and timing of the original YouTube annotations as closely as possible, including shapes, positioning, and text styles.

使用 ASS 格式，Annotations2Sub 可以尽可能接近地复制原始 YouTube 注释的外观和计时，包括形状、定位和文本样式。

---

## Dependencies / 依赖项

Annotations2Sub itself can be installed via pip. However, for some of its functionalities, it relies on external programs:

*   **mpv:** Required for the video preview feature (`-p` or `--preview-video`). mpv is a free, open-source, and cross-platform media player.
*   **FFmpeg:** Required for the video generation feature (`-g` or `--generate-video`), which hardcodes annotations into the video. FFmpeg is a free and open-source software project consisting of a vast software suite of libraries and programs for handling video, audio, and other multimedia files and streams.

Annotations2Sub 本身可以通过 pip 安装。但是，它的某些功能依赖于外部程序：

*   **mpv：** 视频预览功能（`-p` 或 `--preview-video`）需要。mpv 是一款免费、开源、跨平台的媒体播放器。
*   **FFmpeg：** 生成视频功能（`-g` 或 `--generate-video`，将注释硬编码到视频中）需要。FFmpeg 是一个免费的开源软件项目，包含一套用于处理视频、音频和其他多媒体文件和流的庞大软件库和程序。

### Installation / 安装

**Python and pip:**
Annotations2Sub is a Python application. Ensure you have Python (3.6 or newer) and pip installed. You can download Python from [python.org](https://www.python.org/). Pip usually comes with Python installations.

**Python 和 pip：**
Annotations2Sub 是一个 Python 应用程序。请确保你已安装 Python (3.6 或更高版本) 和 pip。你可以从 [python.org](https://www.python.org/) 下载 Python。Pip 通常随 Python 安装包提供。

**mpv:**
*   **Windows:** Download from [mpv.io/installation/](https://mpv.io/installation/) (e.g., using Scoop or Chocolatey).
*   **macOS:** Install via Homebrew: `brew install mpv`
*   **Linux:** Install using your distribution's package manager.
    *   Debian/Ubuntu: `sudo apt update && sudo apt install mpv`
    *   Fedora: `sudo dnf install mpv`
    *   Arch Linux: `sudo pacman -S mpv`

Make sure `mpv` is in your system's PATH after installation.

**mpv：**
*   **Windows：** 从 [mpv.io/installation/](https://mpv.io/installation/) 下载（例如，使用 Scoop 或 Chocolatey）。
*   **macOS：** 通过 Homebrew 安装：`brew install mpv`
*   **Linux：** 使用你的发行版的包管理器安装。
    *   Debian/Ubuntu：`sudo apt update && sudo apt install mpv`
    *   Fedora：`sudo dnf install mpv`
    *   Arch Linux：`sudo pacman -S mpv`

安装后，请确保 `mpv` 在你的系统 PATH 中。

**FFmpeg:**
*   **Windows:** Download pre-built binaries from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) (e.g., from gyan.dev or BtbN). Extract the files and add the `bin` directory (containing `ffmpeg.exe`, `ffprobe.exe`, etc.) to your system's PATH.
*   **macOS:** Install via Homebrew: `brew install ffmpeg`
*   **Linux:** Install using your distribution's package manager.
    *   Debian/Ubuntu: `sudo apt update && sudo apt install ffmpeg`
    *   Fedora: `sudo dnf install ffmpeg`
    *   Arch Linux: `sudo pacman -S ffmpeg`

Make sure `ffmpeg` is in your system's PATH after installation.

**FFmpeg：**
*   **Windows：** 从 [ffmpeg.org/download.html](https://ffmpeg.org/download.html) 下载预编译的二进制文件（例如，从 gyan.dev 或 BtbN）。解压文件并将包含 `ffmpeg.exe`、`ffprobe.exe` 等的 `bin` 目录添加到你的系统 PATH 中。
*   **macOS：** 通过 Homebrew 安装：`brew install ffmpeg`
*   **Linux：** 使用你的发行版的包管理器安装。
    *   Debian/Ubuntu：`sudo apt update && sudo apt install ffmpeg`
    *   Fedora：`sudo dnf install ffmpeg`
    *   Arch Linux：`sudo pacman -S ffmpeg`

安装后，请确保 `ffmpeg` 在你的系统 PATH 中。

After installing these dependencies, you can install Annotations2Sub itself:
安装完这些依赖项后，你可以安装 Annotations2Sub 本身：
```bash
pip install Annotations2Sub
```
You can then verify the installation by running `Annotations2Sub --version`.
然后，你可以通过运行 `Annotations2Sub --version` 来验证安装。
