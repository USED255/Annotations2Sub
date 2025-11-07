# Annotations2Sub

Convert YouTube Annotations to subtitles.

[![License GPLv3](https://img.shields.io/pypi/l/Annotations2Sub?color=1)](https://pypi.org/project/Annotations2Sub/)
[![Test](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml/badge.svg)](https://github.com/USED255/Annotations2Sub/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/USED255/Annotations2Sub/branch/master/graph/badge.svg?token=SSNQNEAXMP)](https://codecov.io/gh/USED255/Annotations2Sub)
[![Version](https://img.shields.io/pypi/v/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)
[![Python version](https://img.shields.io/pypi/pyversions/Annotations2Sub)](https://pypi.org/project/Annotations2Sub)

This document is AI-translated and may contain inaccuracies. Please refer to the Chinese version for accuracy.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
    - [Install Python](#install-python)
    - [Get Original Video](#get-original-video)
    - [Get Annotation Files](#get-annotation-files)
    - [Choose a Player](#choose-a-player)
  - [Installation](#installation)
  - [Convert Annotations](#convert-annotations)
  - [Play Video](#play-video)
  - [Results](#results)
  - [Optional: Embed into Video](#optional-embed-into-video)
- [Command Line Usage](#command-line-usage)
  - [Arguments](#arguments)
  - [Options](#options)
    - [-h View Help](#view-help)
    - [-x -y Transform Resolution](#transform-resolution)
    - [-f Specify Font](#specify-font)
    - [-n No Overwrite Files](#no-overwrite-files)
    - [-o Save to File](#save-to-file)
    - [-O Specify Output Directory](#specify-output-directory)
    - [-v Show Version](#show-version)
    - [-V Verbose Output](#verbose-output)
  - [Return Codes](#return-codes)
- [Limitations](#limitations)
- [Getting Help](#getting-help)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Miscellaneous](#miscellaneous)
  - [Important Updates](#important-updates)
  - [Secondary Development](#secondary-development)
  - [Comparison with Similar Software](#comparison-with-similar-software)
  - [Derivative Projects](#derivative-projects)

## Introduction

YouTube Annotations was a feature launched by YouTube in 2008 that allowed video creators to add text, links, and interactive elements to videos to enhance the viewing experience. YouTube removed this feature in 2019.

ASS subtitles are a common external subtitle format, short for Advanced SubStation Alpha. Compared to other subtitle formats, it can set fonts, colors, positions, and even add images and effects to enhance your viewing experience.

This tool can help you convert YouTube annotations into ASS subtitle files that you can play or add to videos. If you don't need this functionality, it's recommended to use [AnnotationsRestored](https://github.com/isaackd/AnnotationsRestored).

## Getting Started

### Prerequisites

Before you begin, you need to prepare Python, video files, YouTube annotation XML files, a video player, and related background knowledge.

#### Install Python

Python is a widely used high-level programming language. This tool is written in Python, so you need to install Python 3.7 or higher.

##### Windows

1. Open the Start menu, find and open Microsoft Store.
2. Search for Python.
3. Open the details page for Python 3.13 (or another version) and install it.

##### Other

Please visit [Python Setup and Usage](https://docs.python.org/3/using/index.html)

#### Get Original Video

It's recommended to use [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download videos. yt-dlp is a multi-purpose video downloader that can download YouTube videos.

1. Open the Start menu, find and open "Terminal".
2. Paste the following command and press Enter:

```shell
pip install yt-dlp
```

3. Wait for the installation to complete.
4. Use the following command to download a video:

```shell
yt-dlp [replace with your video URL]
```

#### Get Annotation Files

Annotation files are in XML format with a `.xml` extension. You can obtain annotation files through the following methods:

1. Use the [AnnotationsRestored](https://github.com/isaackd/AnnotationsRestored) browser extension.
2. Archives from [Internet Archive](https://archive.org/details/youtubeannotations).
3. Annotation files shared by other users.

It's recommended to use the [AnnotationsRestored](https://github.com/isaackd/AnnotationsRestored) extension to download annotation files. On the video page, click the extension icon, then click "Download".

#### Choose a Player

The following players are recommended as they all support ASS subtitles:

1. [mpv](https://mpv.io/)
2. [VLC](https://www.videolan.org/)
3. [PotPlayer](https://potplayer.daum.net/)
4. [MPC-HC](https://github.com/clsid2/mpc-hc)
5. [SMPlayer](https://www.smplayer.info/)

Different players will render ASS subtitles differently. mpv is recommended.

### Installation

Open a terminal and use pip to install Annotations2Sub:

```shell
pip install Annotations2Sub
```

### Convert Annotations

1. Right-click in the folder containing the annotation file and select "Open in Terminal".
2. Run the command:

```shell
Annotations2Sub annotations.xml
```

The subtitle file will be saved to the same directory as the annotation file.

### Play Video

1. Ensure the video file and the converted .ass subtitle file are in the same directory.
2. Open the video with a player that supports ASS subtitles.
3. The player will automatically load the subtitle file (you can also drag and drop or manually load it via the right-click menu).

### Results

- Annotations should display normally over the video.
- Due to technical limitations, you cannot interact with annotations, including closing annotations, opening links, expanding details, jumping to other videos, pausing, etc.
- Some annotations may display incorrectly or be missing. Please report these issues in [Issues](https://github.com/USED255/Annotations2Sub/issues).

### Optional: Embed into Video

If you want to embed subtitles into the video for publishing to video sites, you can use the following tools:

1. [FFmpeg](https://ffmpeg.org/): Command-line tool, very powerful.

   ```shell
   ffmpeg -i video.mp4 -vf ass=annotations.xml.ass output.mp4
   ```

2. [HandBrake](https://handbrake.fr/): Graphical interface, easy to use.
   - Load the video
   - Import subtitles in the subtitle options
   - Check "Burn In"
   - Start encoding

## Command Line Usage

### Arguments

The argument is one or more file paths to annotation files that need to be converted.

An "annotation file" is an XML document. If you don't have this file, you should refer to the [Get Annotation Files](#get-annotation-files) section.

Example:

```shell
Annotations2Sub annotations.xml
```

Annotations will be converted to an ASS subtitle file and saved to the same directory as the "annotation file".
You can see the effect by loading the video and the output subtitle file with a video player that supports ASS subtitles.

Output:

```text
Saved to: "annotations.xml.ass"
```

### Options

#### View Help

`-h, --help show this help message and exit`

Example:

```shell
Annotations2Sub -h
```

Output:

```shell
usage: Annotations2Sub [-h] [-x 1920] [-y 1080] [-f Microsoft YaHei]
                   [-n] [-o file] [-O directory] [-v] [-V]
                   file [file]

Download and convert Youtube annotations

positional arguments:
  file or videoId       Multiple file paths or video IDs to convert

options:
  -h, --help            show this help message and exit
  -x 1920, --transform-resolution-x 1920
                        Transform resolution X
  -y 1080, --transform-resolution-y 1080
                        Transform resolution Y
  -f Microsoft YaHei, --font Microsoft YaHei
                        Specify font
  -n, --no-overwrite-files
                        Don't overwrite files
  -o file, --output file    Save to this file, if "-" output to stdout
  -O directory, --output-directory directory
                        Specify output directory for converted files
  -v, --version         Show version number
  -V, --verbose         Show more messages
```

#### Transform Resolution

`-x 1920, --transform-resolution-x 1920 Transform resolution X`

`-y 1080, --transform-resolution-y 1080 Transform resolution Y`

Resolution information is only truly needed when drawing "boxes" for highlight-type annotations or label-style annotations, so this parameter is optional.

The subtitle filter will correctly handle the "PlayRes{X,Y}" in the subtitle script. Some subtitle filters used by certain players exhibit strange behavior, such as directly using the Y value for the X axis, which causes rendering errors. In such cases, you need to use this parameter.

Example:

```shell
Annotations2Sub -x 1920 -y 1080 annotations.xml
```

Effect: There may be no obvious change.

#### Specify Font

`-f Microsoft YaHei, --font Microsoft YaHei Specify font`

Annotations use a sans-serif font, but the actual font selected by `font-family: sans-serif` can vary significantly depending on installed fonts, browser, and language environment.
Different subtitle filters handle fonts differently, and different computers use different fonts, so font issues are normal.
You may need to use this parameter when font issues occur.

Example:

```shell
Annotations2Sub -f Arial annotations.xml
```

Effect: The displayed font will change to the font you specified.

#### No Overwrite Files

`-n, --no-overwrite-files Don't overwrite files`

By default, if the output file already exists, it will be overwritten directly. Use the `-n` option to prevent overwriting existing files.

Example:

```shell
Annotations2Sub -n annotations.xml
```

Effect: If `annotations.xml.ass` already exists, the program will skip it and display a warning message.

#### Save to File

`-o file, --output file Save to this file`

Specify the path and name of the output file. If "-" is used as the argument, the subtitle content will be output to stdout.

Example:

```shell
Annotations2Sub annotations.xml -o ../output.ass
```

Effect: The subtitle will be saved to the parent directory, named `output.ass`.

```shell
Annotations2Sub annotations.xml -o -
```

Effect: You will see the subtitle content printed directly in the terminal.

#### Specify Output Directory

`-O directory, --output-directory directory Specify output directory for converted files`

Specify the save directory for all files to be output. Cannot be used simultaneously with the `-o` option.

Example:

```shell
Annotations2Sub annotations1.xml ../annotations2.xml -O output_dir
```

Effect: All subtitle files will be saved to the `output_dir` directory.

#### Show Version

`-v, --version Show version number`

Display the version number of the currently running Annotations2Sub and exit.

Example:

```shell
Annotations2Sub -v
```

Output:

```text
Annotations2Sub v2.24.0
```

#### Verbose Output

`-V, --verbose Show more messages`

Display more warning messages.

Example:

```shell
Annotations2Sub -V annotations.xml
```

Effect: Will print the reasons why certain annotations were not converted, as well as stack traces for XML parsing exceptions.

### Return Codes

- 0: Success
- 2: Argument error
- 13: Not a file
- 14: Not an Annotations file
- 15: Invalid XML document
- 18: Multiple errors
- 19: Unknown error
- 20: Empty file

## Limitations

- Cannot interact with annotations, including but not limited to closing annotations, opening links, expanding details, jumping to other videos, pausing, etc.
- Effects will vary depending on the player and subtitle filter.
- Cannot accurately typeset text.
- Some annotations may display incorrectly or be missing.

## Getting Help

If you encounter problems or need help, please open an [Issue](https://github.com/USED255/Annotations2Sub/issues).

## Contributing

Any contributions are welcome, even if it's just changing a single character! Even if you don't know how to program, you can report bugs or ask me questions, so I know what else can be improved.
If you want to start programming, you can read [Annotations2Sub Source Code](src/README.md) to understand the project structure and code style.

## License

This project is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html). See the [LICENSE](LICENSE) file for details.

## Acknowledgments

[omarroth](https://archive.org/details/youtubeannotations)

Created the YouTube Annotations Archive project, preserving this content that was about to disappear, which was a necessary condition for this work to be carried out.

[Nirbheek Chauhan](https://github.com/nirbheek/youtube-ass)

Created the earliest YouTube annotation conversion tool. One of the original purposes of this project was to fix its ASS implementation issues.

[Zhenye Wei](https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范)

Compiled detailed ASS subtitle format documentation and even pointed out issues with subtitle filters.

[Invidious](https://invidious.io/)

Provided an alternative API for YouTube, used for downloading and previewing videos.

[Isaac](https://github.com/isaackd/annotationlib)

The "simple format" of annotationlib inspired the software architecture.

[Eva](https://github.com/po5/assnotations)

Referenced their code to solve some difficult problems.

[Internet Archive](https://archive.org/)

The Internet Archive provided foundational support for preserving YouTube annotations. This project downloaded annotation archives and historical versions of YouTube from it.

[Gemini 1.5 Pro](https://deepmind.google/models/gemini/pro/)

Used its 1M context capability to help reverse engineer annotation-related files in YouTube web pages.

[Rain Shimotsuki](https://www.youtube.com/@rain_shimotsuki)

Their videos and annotations were the initial motivation for this project.

[KeksusGSPB](https://www.youtube.com/watch?v=c1iCjpxDxz4)

Used their annotations as a regression baseline.

[XNX.ROmania](https://web.archive.org/web/20230227230532/https://www.youtube.com/watch?v=M2ryDEyyrXE).

"The last annotations on YouTube" demonstrated the capabilities of annotations and provided a reference for correctly implementing annotation effects.

## [Back to Top](#table-of-contents)

## Miscellaneous

### Important Updates

- v2.23.0: Removed annotation downloading, preview, and video generation features because the services they depended on are no longer available.

### Secondary Development

```Python
# You can import Annotations2Sub as a package:
from Annotations2Sub import *

"""
Annotations2Sub exports the following:
"version"
"Run"
"Parse"
"Annotation"
"Convert"
"Subtitles"
"Style"
"Event"
"NotAnnotationsDocumentError"
"AnnotationsXmlStringToSubtitlesString"
Please refer to the corresponding docstrings for specific instructions.
"""

# Example: Read annotations from a file and convert to subtitles
with open('annotations.xml', 'r', encoding='utf-8') as f:
    xml_string = f.read()

# Convert XML string to subtitle string
subtitles_string = AnnotationsXmlStringToSubtitlesString(xml_string)

# Save subtitle file
with open('output.ass', 'w', encoding='utf-8') as f:
    f.write(subtitles_string)

# If you're concerned about licensing issues, you can contact me for an alternative license.
```

### Comparison with Similar Software

Currently, the only actively maintained similar software is [AnnotationsRestored](https://github.com/isaackd/AnnotationsRestored).

AnnotationsRestored:

- As a browser extension, it can directly restore and display annotations in the browser with no technical barrier.
- Supports interactive features such as clicking links, expanding details, etc., closer to the original YouTube annotation experience.
- Suitable for online viewing and browsing annotations.

Annotations2Sub:

- Saves annotations as subtitle files that can be edited again.
- Suitable for redistributing videos with annotations.

Recommendations:

- If you just want to watch videos with annotations, use AnnotationsRestored.
- If you need to re-edit videos, use Annotations2Sub.
- Different annotations may perform differently on the two software, use the best software according to the situation.

### Derivative Projects

[youtube_annotations_hack](https://github.com/USED255/youtube_annotations_hack)

Retrieved old YouTube web pages from archive.org, modified them to run locally, then deobfuscated with LLM. Can correctly reproduce YouTube Annotations while debugging.

[Youtube Annotations Text](https://huggingface.co/datasets/used255/youtube_annotations_text)

Extracted text from 1.3 billion annotation archives.

[Youtube Annotations video metadata](https://archive.org/details/youtube_annotations_video_metadata)

Metadata database of videos with annotations.

[Annotations2Sub-Lite](https://a2s.liutao.page/)

A web version made by AI.
