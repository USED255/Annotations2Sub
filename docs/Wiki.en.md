# Introduction

Annotations2Sub is a tool designed to download and convert YouTube annotations. As YouTube has removed the annotation feature, this tool provides a way to preserve and access this content.

Its primary purpose is to fetch annotation files (in XML format) and convert them into a subtitle format.

Key features include:
* Downloading annotation files from YouTube (if available) or the Internet Archive.
* Converting annotation XML files into subtitle formats.
* Option to specify video resolution for conversion.
* Option to specify font for subtitles.
* Ability to preview generated subtitles with a video using `mpv`.
* Ability to generate a video with embedded subtitles using `FFmpeg`.
* Support for using Invidious instances to fetch annotation data.

## Command-Line Interface (CLI)

The primary way to use Annotations2Sub is through its command-line interface.

### Synopsis

```
usage: Annotations2Sub.py [-h] [-l] [-x 100] [-y 100] [-f Arial ] [-o Folder] [-d]
                          [-i invidious.domain] [-p] [-g] [-s] [-n] [-k] [-u] [-v]
                          [-V]
                          File or videoId [File or videoId ...]
```

### Positional Arguments

*   `File or videoId`: Specifies the file path(s) to local annotation XML file(s) or YouTube video ID(s) to be processed. Multiple files or video IDs can be provided.

### Optional Arguments

*   `-h, --help`: Show the help message and exit.
*   `-x 100, --transform-resolution-x 100`: Transform resolution X. Sets the horizontal resolution for the output. Default is 100.
*   `-y 100, --transform-resolution-y 100`: Transform resolution Y. Sets the vertical resolution for the output. Default is 100.
*   `-f Arial, --font Arial`: Specify font to be used for the subtitles. Default is "Arial".
*   `-d, --download-for-archive`: Try to download the Annotations file from the Internet Archive.
*   `-D, --download-annotations-only`: Download Annotations only. No conversion will be performed.
*   `-p, --preview-video`: Preview video with generated subtitles. Requires `mpv` (https://mpv.io/) to be installed.
*   `-g, --generate-video`: Generate a video with the subtitles embedded. Requires `FFmpeg` (https://ffmpeg.org/) to be installed.
*   `-i invidious-instances.domain, --invidious-instances invidious-instances.domain`: Specify Invidious instances (e.g., `invidious.snopyta.org`) to use for downloading. See https://redirect.invidious.io/ for a list of instances.
*   `-n, --no-overwrite-files`: Do not overwrite existing files. If an output file already exists, the tool will not proceed with writing to it.
*   `-N, --no-keep-intermediate-files`: Do not keep intermediate files that are generated during processing (e.g., downloaded XML files if conversion is also done).
*   `-O directory, --output-directory directory`: Specify the output directory for the converted files.
*   `-o File, --output File`: Specify the output file name. If "-", the output will be sent to standard output. This is typically used when processing a single input.
*   `-v, --version`: Show the program's version number and exit.
*   `-V, --verbose`: Show more detailed messages during processing.

### Examples

1.  **Convert a local annotation file:**
    ```bash
    Annotations2Sub 29-q7YnyUmY.xml
    ```

2.  **Download and convert annotations for a YouTube video:**
    (This will attempt to download from YouTube first, then from the Internet Archive if `-d` is also specified)
    ```bash
    Annotations2Sub 29-q7YnyUmY
    ```

3.  **Download annotations for a YouTube video from the Internet Archive and convert them:**
    ```bash
    Annotations2Sub -d 29-q7YnyUmY
    ```

4.  **Generate a video with embedded subtitles:**
    ```bash
    Annotations2Sub -g 29-q7YnyUmY
    ```

5.  **Download annotations using a specific Invidious instance and save to a specific output directory:**
    ```bash
    Annotations2Sub -i invidious.snopyta.org -O ./my_annotations 29-q7YnyUmY
    ```

6.  **Convert a local file, specifying output resolution and font:**
    ```bash
    Annotations2Sub -x 1920 -y 1080 -f "Times New Roman" my_video_annotations.xml
    ```

## Core Functionality and Workflow

Annotations2Sub processes YouTube annotation files (typically `annotations.xml`) and converts them into subtitle formats like Advanced SubStation Alpha (`.ass`). The general workflow is as follows:

1.  **Input**:
    *   The primary input is an XML file containing the YouTube annotations data (`Annotations.xml`).
    *   This file can be a local file or downloaded using a video ID. The tool can fetch this from YouTube directly (if still available for that video), or from archives like the Internet Archive or via Invidious instances.

2.  **Parsing**:
    *   The raw XML data (read from the file or download stream) is parsed using Python's `xml.etree.ElementTree.fromstring()` function. This converts the XML string into an `Element` object, which is a tree-like representation of the XML structure.
    *   This `Element` object is then processed by a custom `Parse()` function. This function traverses the XML tree and extracts relevant annotation data (text, timing, position, style, etc.), converting it into a list of structured `Annotation` objects (`List[Annotation]`). Each `Annotation` object represents a single annotation event or element from the original YouTube annotations.

3.  **Conversion**:
    *   The `List[Annotation]` obtained from the parsing step is then passed to a `Convert()` function.
    *   This function takes the structured annotation data and transforms it into a list of subtitle `Event` objects (`List[Event]`). An `Event` typically represents a single line or block of text in the output subtitle file, with its associated timing (start and end) and styling information.
    *   During this stage, styling information from the annotations (like position, color, font size which were part of the original YouTube annotation system) is translated into equivalent styling directives for the target subtitle format (e.g., ASS tags).

4.  **Output Generation**:
    *   The `List[Event]`, along with any necessary header information and style definitions (often encapsulated in a `Sub` object, which might also contain `Style` objects), is then formatted into a string that conforms to the chosen subtitle file format.
    *   The most common output format is `.ass` (Advanced SubStation Alpha), which supports rich styling and positioning.
    *   The final string is then written to an output file (e.g., `video_annotations.ass`) or to standard output.

The process can be visualized as:

```
[Annotations.xml file] --(read file)--> [XML String] --(xml.etree.ElementTree.fromstring())--> [Element object]
                                                                                                     |
                                                                                                     | Parse()
                                                                                                     ▼
                                                                                           [List of Annotation objects]
                                                                                                     |
                                                                                                     | Convert()
                                                                                                     ▼
                                                                                           [List of Event objects (subtitle events)]
                                                                                                     |
                                                                                                     | (str(Sub) / Format to string)
                                                                                                     ▼
                                                                                           [Output String (e.g., .ass format)] --(write file)--> [Annotations.ass file]
```

### Additional Capabilities

Beyond this core conversion workflow, Annotations2Sub offers several related functionalities, typically accessed via CLI options:

*   **Video Preview**: Using `mpv`, the tool can display a video along with the generated subtitles for immediate preview.
*   **Video Generation**: Using `FFmpeg`, Annotations2Sub can create a new video file with the subtitles hardcoded (burned in) onto the video frames.
*   **Downloading**: As mentioned, it includes robust options for downloading annotation files, including from the Internet Archive and Invidious instances, which is crucial since YouTube has removed direct access to annotations.

## Dependencies and Installation

### Main Tool Installation

Annotations2Sub is a Python package and can be easily installed using `pip`:

```bash
pip install Annotations2Sub
```

This command will download Annotations2Sub from the Python Package Index (PyPI) and install it along with its Python dependencies.

### External Dependencies

For some features, Annotations2Sub relies on external command-line tools that need to be installed separately on your system:

*   **FFmpeg** (`https://ffmpeg.org/`):
    *   **Purpose**: Required for the video generation feature (`-g` or `--generate-video` option). FFmpeg is used to take an input video and embed the converted annotations as hardcoded subtitles into a new video file.
    *   **Installation**: Download from the FFmpeg website and install it according to your operating system's instructions. Ensure it's added to your system's PATH so that `Annotations2Sub` can call it.

*   **mpv** (`https://mpv.io/`):
    *   **Purpose**: Required for the video preview feature (`-p` or `--preview-video` option). `mpv` is a media player that is used to play the original video with the generated subtitle file for quick checking.
    *   **Installation**: Download from the mpv website and install it. Ensure it's available in your system's PATH.

If you do not need video generation or preview capabilities, you do not need to install FFmpeg or mpv. The core annotation downloading and conversion functionalities will still work.

## Project History and Motivation

The inception of Annotations2Sub was a direct response to YouTube's decision to discontinue annotations in January 2019. The author, an avid YouTube user, discovered that annotations, crucial for content like translated lyrics in music videos, were disappearing. This led to a strong desire to preserve this unique form of content.

**Initial Spark and Learning Curve:**
Upon learning that annotation data was archived by entities like the Internet Archive, the author sought tools to convert these XML files into a usable subtitle format (like Advanced SubStation Alpha - ASS). Existing tools, such as `youtube-ass`, were found to be inadequate, lacking features like color and proper positioning, or were simply difficult to use.

Despite not having a programming background at the time, the author was motivated to create a better solution. This marked the beginning of a learning journey into programming, with the initial goal of making the archived annotations usable.

**Development Milestones:**
*   **Early Versions:** The first functional versions were inspired by `youtube-ass` and basic ASS format specifications. Techniques like "style override codes" were employed to handle annotation positioning and colors.
*   **Feature Enhancements:** Support for "popup" style annotations was added using a "drawing mode." Integration with Invidious (for fetching annotation data) and FFmpeg/mpv (for video generation and preview) significantly expanded the tool's capabilities.
*   **Overcoming Challenges:** The development process wasn't without hurdles. Accurately replicating complex CSS-like positioning from YouTube annotations proved difficult. Attempts to refactor the code for better modularity (e.g., separating parsing from generation, inspired by `annotationlib`) were part of an iterative refinement process.
*   **Renewed Focus (2022):** A period of dedicated work led to significant improvements in code structure, including modularization, the addition of unit tests, type checking, and overall code quality enhancements with detailed comments.
*   **Leveraging Archives:** The discovery of archived old YouTube webpages on the Internet Archive provided a valuable resource for debugging and understanding the correct visual representation of annotations. Furthermore, processing a large Zstandard-compressed tarball of YouTube annotations from `archive.omar.yt` into an SQLite database enhanced the tool's robustness in handling diverse annotation files.

The project, born out of a personal need to preserve a disappearing feature of the internet, evolved into a comprehensive tool, with the author learning to code along the way. It stands as a testament to the desire to archive and maintain access to digital heritage.

## Troubleshooting and Known Issues

### General Disclaimer

**Important:** As stated in the project's `README.md`:
> Because of the ever-changing behavior and quirks of subtitle filters, and the vast differences between web and subtitle technologies, this project was unable to correctly restore the behavior of annotations.

While Annotations2Sub strives to convert YouTube annotations as accurately as possible, users should be aware that a perfect 1:1 replication of the original browser rendering is often not achievable. This is due to:
*   Fundamental differences between how web browsers render content (HTML, CSS, JavaScript) and how subtitle formats (like ASS) display text and graphics.
*   The complexity and sometimes inconsistent behavior of YouTube's original annotation system.
*   Variations in how different video players interpret subtitle styling.

### Common Issues and Solutions

1.  **Video Generation/Preview Not Working:**
    *   **Issue:** The `-g` (generate video) or `-p` (preview video) options produce errors or don't work.
    *   **Solution:** Ensure that **FFmpeg** (for `-g`) and/or **mpv** (for `-p`) are correctly installed on your system and, crucially, that their executable locations are included in your system's `PATH` environment variable. Refer to the "Dependencies and Installation" section for more details.

2.  **Font-Related Issues:**
    *   **Issue:** Subtitles appear with incorrect fonts, or special characters are not displayed correctly.
    *   **Solution:**
        *   The default font used is "Arial". If this font is not available on your system, a fallback font will be used, which might alter the appearance. You can specify a different font using the `-f` or `--font` command-line option (e.g., `-f "Times New Roman"`).
        *   Ensure the chosen font supports all necessary characters for the language of the annotations. For some languages or special symbols, a more comprehensive font might be needed.
        *   The way fonts are handled can also depend on the subtitle rendering engine of the video player you are using.

3.  **Issues with Specific Annotation Files:**
    *   **Issue:** A particular `annotations.xml` file fails to convert or produces garbled output.
    *   **Solution:** While the tool has been tested with a wide range of annotation files, including a large database from archives, some very old, uniquely structured, or potentially corrupt annotation XML files might not process perfectly. If you encounter such a file, you can consider reporting it as an issue on the project's repository, providing the problematic XML file if possible.

4.  **Invidious Instance Issues:**
    *   **Issue:** Downloading annotations via an Invidious instance (`-i` option) fails.
    *   **Solution:** Invidious instances are community-hosted and their availability can change. If one instance is not working, try a different one from the public list (e.g., https://redirect.invidious.io/). Some instances might be slow or overloaded.

5.  **Incorrect Visual Representation:**
    *   **Issue:** The position, size, or style of annotations in the subtitle output doesn't perfectly match how they appeared on YouTube.
    *   **Solution:** This is related to the general disclaimer. The conversion process involves translating web-based rendering logic to subtitle system logic, which can lead to discrepancies. The tool attempts a best-effort conversion. Adjusting resolution parameters (`-x`, `-y`) might sometimes help for scaling issues, but complex interactive or heavily styled annotations are particularly challenging to replicate perfectly.

If you encounter persistent issues, checking the program's output for error messages (using the `-V` or `--verbose` option for more details) can provide clues.

## Contributing

Contributions to Annotations2Sub are highly welcome! Whether you have suggestions, bug reports, or want to contribute code, your help is appreciated.

Please visit the project's [GitHub page](https://github.com/USED255/Annotations2Sub) for more information. There you can:
*   Check for existing issues or report new ones.
*   Suggest new features or enhancements.
*   Submit pull requests with your contributions.

If you plan to contribute code, it's a good idea to first discuss your proposed changes via an issue, especially for larger contributions.

## License

Annotations2Sub is licensed under the [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html).
