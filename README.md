# Annotations2Sub

下载和转换 Youtube 注释

Download and convert Youtube Annotations

[![License GPLv3](https://img.shields.io/pypi/l/Annotations2Sub?color=1)](https://pypi.org/project/Annotations2Sub/)
[![Test](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml/badge.svg)](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/USED255/Annotations2Sub/branch/master/graph/badge.svg?token=SSNQNEAXMP)](https://codecov.io/gh/USED255/Annotations2Sub)
[![Version](https://img.shields.io/pypi/v/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)
[![Python version](https://img.shields.io/pypi/pyversions/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)

---

## The Problem

YouTube annotations were a popular feature that allowed creators to add interactive commentary, links, and other information directly into their videos. However, YouTube deprecated this feature in 2019, and all existing annotations were removed. This resulted in the loss of a significant amount of creative content and valuable information.

Annotations2Sub helps address this problem by providing a way to download and convert YouTube annotations into the ASS subtitle format. This allows you to preserve and view annotations even though they are no longer available on YouTube.

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

## Usage Examples

### Convert a local annotations file

If you have an annotations XML file saved locally, you can convert it to ASS format:

```bash
Annotations2Sub annotations.xml
```

### Download and convert annotations for a video ID

You can directly download and convert annotations for a given YouTube video ID:

```bash
Annotations2Sub -d 29-q7YnyUmY
```

This will attempt to fetch the annotations from the Internet Archive.

### Specify output directory

To save the converted ASS file to a specific directory:

```bash
Annotations2Sub -d 29-q7YnyUmY -O /path/to/output/directory/
```

### Specify output filename

To save the converted ASS file with a specific name:

```bash
Annotations2Sub -d 29-q7YnyUmY -o my_video_annotations.ass
```

### Download annotations only

If you only want to download the raw annotation XML file without converting it:

```bash
Annotations2Sub -D 29-q7YnyUmY
```

### Preview video with annotations (requires mpv)

To preview a video with the generated annotations using mpv:

```bash
Annotations2Sub -p 29-q7YnyUmY
```
This will download the annotations, convert them, and then launch mpv to play the video with the subtitles. You need to have the video file locally or provide a URL to the video.

### Generate video with hardcoded annotations (requires FFmpeg)

To create a new video file with the annotations burned into the video (hardsubs):

```bash
Annotations2Sub -g 29-q7YnyUmY
```
This also requires the original video to be available locally or via a URL. FFmpeg will be used to process the video.

### Using a specific Invidious instance

If you want to use a specific Invidious instance for fetching information (useful if the default is blocked or slow):
```bash
Annotations2Sub -d 29-q7YnyUmY -i invidious.snopyta.org
```

### Adjusting resolution for conversion

Annotations are often tied to the resolution of the video they were created for. If the default (100x100) is not suitable, you can specify the target video resolution:

```bash
Annotations2Sub -d 29-q7YnyUmY -x 1920 -y 1080
```
This helps in scaling the annotation elements correctly in the ASS file.

### Specifying font

You can specify a font to be used in the ASS file:
```bash
Annotations2Sub -d 29-q7YnyUmY -f "Comic Sans MS"
```
Make sure the font is available on the system where the subtitles will be viewed.

---

## Output Format: ASS Subtitles

Annotations2Sub converts YouTube annotations into the **Advanced SubStation Alpha (ASS)** subtitle format. ASS is a powerful subtitle format that allows for advanced features like:

*   **Styled text:** Control over font, size, color, bold, italics, etc.
*   **Positioning:** Precise placement of subtitles on the screen.
*   **Drawing commands:** Ability to draw vector shapes (used by Annotations2Sub to replicate annotation boxes and speech bubbles).
*   **Timing:** Accurate synchronization of subtitles with video frames.
*   **Layers:** Control over how overlapping subtitles are displayed.

ASS files are plain text files with a `.ass` extension. They can be played with most modern video players, such as VLC, mpv, MPC-HC, and PotPlayer. Many video players will automatically load ASS files if they have the same name as the video file and are in the same directory.

The use of ASS format allows Annotations2Sub to replicate the appearance and timing of the original YouTube annotations as closely as possible, including shapes, positioning, and text styles.

---

## Dependencies

Annotations2Sub itself can be installed via pip. However, for some of its functionalities, it relies on external programs:

*   **mpv:** Required for the video preview feature (`-p` or `--preview-video`). mpv is a free, open-source, and cross-platform media player.
*   **FFmpeg:** Required for the video generation feature (`-g` or `--generate-video`), which hardcodes annotations into the video. FFmpeg is a free and open-source software project consisting of a vast software suite of libraries and programs for handling video, audio, and other multimedia files and streams.

### Installation

**Python and pip:**
Annotations2Sub is a Python application. Ensure you have Python (3.6 or newer) and pip installed. You can download Python from [python.org](https://www.python.org/). Pip usually comes with Python installations.

**mpv:**
*   **Windows:** Download from [mpv.io/installation/](https://mpv.io/installation/) (e.g., using Scoop or Chocolatey).
*   **macOS:** Install via Homebrew: `brew install mpv`
*   **Linux:** Install using your distribution's package manager.
    *   Debian/Ubuntu: `sudo apt update && sudo apt install mpv`
    *   Fedora: `sudo dnf install mpv`
    *   Arch Linux: `sudo pacman -S mpv`

Make sure `mpv` is in your system's PATH after installation.

**FFmpeg:**
*   **Windows:** Download pre-built binaries from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) (e.g., from gyan.dev or BtbN). Extract the files and add the `bin` directory (containing `ffmpeg.exe`, `ffprobe.exe`, etc.) to your system's PATH.
*   **macOS:** Install via Homebrew: `brew install ffmpeg`
*   **Linux:** Install using your distribution's package manager.
    *   Debian/Ubuntu: `sudo apt update && sudo apt install ffmpeg`
    *   Fedora: `sudo dnf install ffmpeg`
    *   Arch Linux: `sudo pacman -S ffmpeg`

Make sure `ffmpeg` is in your system's PATH after installation.

After installing these dependencies, you can install Annotations2Sub itself:
```bash
pip install Annotations2Sub
```
You can then verify the installation by running `Annotations2Sub --version`.
