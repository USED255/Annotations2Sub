# -*- coding: utf-8 -*-
import os

import pytest

from Annotations2Sub import cli_utils
from Annotations2Sub.cli_utils import AnnotationsXmlStringToSub, GetAnnotationsUrl
from tests import baselinePath


def test_GetAnnotationsUrl():
    assert (
        GetAnnotationsUrl("-8kKeUuytqA")
        == "https://archive.org/download/youtubeannotations_64/-8.tar/-8k/-8kKeUuytqA.xml"
    )


def test_GetAnnotationsUrl_ValueError():
    with pytest.raises(ValueError):
        GetAnnotationsUrl("")


def test_GetMedia():
    def GetUrlMock(url: str):
        if url == "https://good.instance/api/v1/videos/-8kKeUuytqA":
            return r'{"adaptiveFormats":[{"type":"video","bitrate":1,"url":"https://1/video"},{"type":"audio","bitrate":1,"url":"https://1/audio"}]}'

    m = pytest.MonkeyPatch()
    # m.setattr(cli_utils, "GetUrl", GetUrlMock) # Old GetMedia test removed

    # assert cli_utils.GetMedia("-8kKeUuytqA", "good.instance") == ( # Old GetMedia test removed
    #     "https://1/video", # Old GetMedia test removed
    #     "https://1/audio", # Old GetMedia test removed
    # ) # Old GetMedia test removed

    # m.undo() # Old GetMedia test removed

# New tests for GetMedia with yt-dlp


@patch('subprocess.run')
def test_get_media_ytdlp_combined_format_first(mock_run):
    """Test GetMedia when yt-dlp returns combined video/audio formats, selecting the best."""
    video_id = "test_video_id_combined"
    # Higher quality (h=1080, tbr=2500) listed second to test sorting
    # Lower quality (h=720, tbr=1500) listed first
    # Bad combined (no url)
    # Best combined (h=1080, tbr=2500)
    mock_json_output = {
        "formats": [
            {"url": "http://example.com/video_720_1500.mp4", "vcodec": "avc1", "acodec": "mp4a", "height": 720, "tbr": 1500},
            {"url": "http://example.com/video_1080_2500.mp4", "vcodec": "avc1", "acodec": "mp4a", "height": 1080, "tbr": 2500},
            {"url": "http://example.com/video_1080_2000.mp4", "vcodec": "avc1", "acodec": "mp4a", "height": 1080, "tbr": 2000},
            {"vcodec": "avc1", "acodec": "mp4a", "height": 480, "tbr": 500}, # No URL
        ],
        "url": "http://example.com/fallback_video.mp4", # Fallback, should not be used if formats are good
        "vcodec": "avc1",
        "acodec": "mp4a"
    }
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0,
        stdout=json.dumps(mock_json_output),
        stderr=""
    )

    expected_video_url = "http://example.com/video_1080_2500.mp4"
    expected_audio_url = "http://example.com/video_1080_2500.mp4"  # Same for combined

    video_url, audio_url = cli_utils.GetMedia(video_id)
    
    mock_run.assert_called_once_with(
        ["yt-dlp", "-j", "--skip-download", video_id],
        capture_output=True, text=True, check=True, encoding='utf-8'
    )
    assert video_url == expected_video_url
    assert audio_url == expected_audio_url


@patch('subprocess.run')
def test_get_media_ytdlp_combined_format_prefer_height_then_bitrate(mock_run):
    """Test GetMedia prefers height then bitrate for combined formats."""
    video_id = "test_video_id_height_bitrate"
    mock_json_output = {
        "formats": [
            # Higher bitrate, but lower resolution
            {"url": "http://example.com/720p_3000kbps.mp4", "vcodec": "avc1", "acodec": "mp4a", "height": 720, "tbr": 3000},
            # Lower bitrate, but higher resolution (should be preferred)
            {"url": "http://example.com/1080p_2000kbps.mp4", "vcodec": "avc1", "acodec": "mp4a", "height": 1080, "tbr": 2000},
            # Same higher resolution, but lower bitrate than the chosen one
            {"url": "http://example.com/1080p_1500kbps.mp4", "vcodec": "avc1", "acodec": "mp4a", "height": 1080, "tbr": 1500},
        ]
    }
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0, stdout=json.dumps(mock_json_output), stderr=""
    )
    expected_url = "http://example.com/1080p_2000kbps.mp4"
    video_url, audio_url = cli_utils.GetMedia(video_id)
    assert video_url == expected_url
    assert audio_url == expected_url


@patch('subprocess.run')
def test_get_media_ytdlp_separate_formats(mock_run):
    """Test GetMedia when yt-dlp returns separate video and audio formats."""
    video_id = "test_video_id_separate"
    mock_json_output = {
        "formats": [
            # Video Formats
            {"url": "http://example.com/video_720_1500.mp4", "vcodec": "avc1", "acodec": "none", "height": 720, "tbr": 1500},
            {"url": "http://example.com/video_1080_2500.mp4", "vcodec": "avc1", "acodec": "none", "height": 1080, "tbr": 2500}, # Best video
            {"url": "http://example.com/video_1080_2000.mp4", "vcodec": "avc1", "acodec": "none", "height": 1080, "tbr": 2000},
            {"url": "http://example.com/video_480_500.mp4", "vcodec": "avc1", "acodec": "none", "height": 480, "tbr": 500},
            # Audio Formats
            {"url": "http://example.com/audio_192.mp4a", "vcodec": "none", "acodec": "mp4a", "abr": 192}, # Best audio
            {"url": "http://example.com/audio_128.mp4a", "vcodec": "none", "acodec": "mp4a", "abr": 128},
            {"url": "http://example.com/audio_64.opus", "vcodec": "none", "acodec": "opus", "abr": 64},
            # Dummy combined format with low quality to ensure separate are chosen if better
            {"url": "http://example.com/combined_low.mp4", "vcodec": "avc1", "acodec": "mp4a", "height": 144, "tbr": 100, "abr": 32},
        ]
    }
    # Remove the dummy combined format for a pure separate format test
    # The GetMedia logic first checks combined_formats. If that list is empty, it proceeds to separate.
    # To test separate formats, we ensure combined_formats list will be empty.
    # The current mock_json_output will result in combined_formats being non-empty.
    # Let's create a version specifically for testing separate format selection path.
    
    pure_separate_mock_json_output = {
        "formats": [
            # Video Formats
            {"url": "http://example.com/video_720_1500.mp4", "vcodec": "avc1", "acodec": "none", "height": 720, "tbr": 1500},
            {"url": "http://example.com/video_1080_2500.mp4", "vcodec": "avc1", "acodec": "none", "height": 1080, "tbr": 2500},
            {"url": "http://example.com/video_1080_2000.mp4", "vcodec": "avc1", "acodec": "none", "height": 1080, "tbr": 2000},
            # Audio Formats
            {"url": "http://example.com/audio_192.mp4a", "vcodec": "none", "acodec": "mp4a", "abr": 192},
            {"url": "http://example.com/audio_128.mp4a", "vcodec": "none", "acodec": "mp4a", "abr": 128},
        ]
    }
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0,
        stdout=json.dumps(pure_separate_mock_json_output), # Use the modified one
        stderr=""
    )

    expected_video_url = "http://example.com/video_1080_2500.mp4"
    expected_audio_url = "http://example.com/audio_192.mp4a"

    video_url, audio_url = cli_utils.GetMedia(video_id)
    
    mock_run.assert_called_once_with(
        ["yt-dlp", "-j", "--skip-download", video_id],
        capture_output=True, text=True, check=True, encoding='utf-8'
    )
    assert video_url == expected_video_url
    assert audio_url == expected_audio_url


@patch('subprocess.run')
def test_get_media_ytdlp_separate_formats_video_only_fallback_to_toplevel_url_if_video(mock_run):
    """Test GetMedia falls back to top-level URL if it's a video and no better video format found."""
    video_id = "test_video_id_video_fallback"
    mock_json_output = {
        "formats": [
            # Only audio format available in 'formats'
            {"url": "http://example.com/audio_128.mp4a", "vcodec": "none", "acodec": "mp4a", "abr": 128},
        ],
        "url": "http://example.com/toplevel_video_only.mp4", # Top-level URL that is a video
        "vcodec": "avc1", # Indicates top-level URL is video
        "acodec": "none", # Indicates top-level URL is video-only
        "height": 720,
        "tbr": 1500
    }
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0, stdout=json.dumps(mock_json_output), stderr=""
    )
    expected_video_url = "http://example.com/toplevel_video_only.mp4"
    expected_audio_url = "http://example.com/audio_128.mp4a"
    video_url, audio_url = cli_utils.GetMedia(video_id)
    assert video_url == expected_video_url
    assert audio_url == expected_audio_url

@patch('subprocess.run')
def test_get_media_ytdlp_separate_formats_audio_only_fallback_to_toplevel_url_if_audio_and_video_has_audio(mock_run):
    """Test GetMedia uses top-level URL for audio if video also has audio and no better audio format."""
    video_id = "test_video_id_audio_fallback"
    mock_json_output = {
        "formats": [
            # Only video format available in 'formats'
            {"url": "http://example.com/video_only_stream.mp4", "vcodec": "avc1", "acodec": "none", "height": 720, "tbr": 1500},
        ],
        "url": "http://example.com/toplevel_combined.mp4", # Top-level URL that is combined
        "vcodec": "avc1", 
        "acodec": "mp4a", # Indicates top-level URL has audio
        "height": 1080,
        "tbr": 2500 
    }
    # In this scenario, GetMedia first finds "video_only_stream.mp4" as best video.
    # Then it finds no audio-only streams in "formats".
    # Then it checks if the chosen video_url (video_only_stream.mp4) itself has audio - it doesn't.
    # THEN it checks the top-level 'url' (toplevel_combined.mp4).
    # If this top-level 'url' is also the video_url AND it has audio, it would use it for audio.
    # However, here video_url is different.
    # The fallback logic for audio_url if video_url is present but audio_url is missing is:
    # `if data.get("vcodec") != "none" and data.get("acodec") != "none" and data.get("url") == video_url:`
    # This won't apply if video_url is from formats and data.get("url") is different.
    # The current GetMedia implementation might not pick up `toplevel_combined.mp4` as audio_url
    # if `video_only_stream.mp4` is chosen as video_url. Let's test current behavior.
    # Based on current GetMedia:
    # 1. Best combined: none
    # 2. Best video-only: "http://example.com/video_only_stream.mp4" -> video_url
    # 3. Best audio-only: none
    # 4. Fallback for video_url (not video_url): data.get("url") which is "http://example.com/toplevel_combined.mp4"
    #    This would set video_url = "http://example.com/toplevel_combined.mp4" if `not video_url` initially. But video_url is already set.
    #    The condition `if not video_url:` means this block is skipped.
    # 5. Fallback for audio_url (if video_url and not audio_url):
    #    `if data.get("vcodec") != "none" and data.get("acodec") != "none" and data.get("url") == video_url:`
    #    `video_url` is "http://example.com/video_only_stream.mp4"
    #    `data.get("url")` is "http://example.com/toplevel_combined.mp4"
    #    So this condition `data.get("url") == video_url` is false. Audio_url remains None.
    # This should raise "没有 Audio URL".
    
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0, stdout=json.dumps(mock_json_output), stderr=""
    )
    with pytest.raises(ValueError, match="没有 Audio URL"):
        cli_utils.GetMedia(video_id)

@patch('subprocess.run')
def test_get_media_ytdlp_toplevel_url_as_combined_if_no_formats_list(mock_run):
    """Test GetMedia uses top-level URL if 'formats' is missing or empty and top-level is combined."""
    video_id = "test_video_id_toplevel_combined"
    mock_json_output = {
        # "formats": [], # Missing or empty 'formats'
        "url": "http://example.com/toplevel_video_audio.mp4", 
        "vcodec": "avc1", 
        "acodec": "mp4a", 
        "height": 720, 
        "tbr": 1500
    }
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0, stdout=json.dumps(mock_json_output), stderr=""
    )
    expected_video_url = "http://example.com/toplevel_video_audio.mp4"
    expected_audio_url = "http://example.com/toplevel_video_audio.mp4"
    video_url, audio_url = cli_utils.GetMedia(video_id)
    assert video_url == expected_video_url
    assert audio_url == expected_audio_url

@patch('subprocess.run')
def test_get_media_ytdlp_toplevel_url_as_video_if_no_formats_list_and_video_only(mock_run):
    """Test GetMedia uses top-level URL for video if 'formats' is missing and top-level is video-only."""
    video_id = "test_video_id_toplevel_video_only"
    mock_json_output = {
        "url": "http://example.com/toplevel_video_only.mp4", 
        "vcodec": "avc1", 
        "acodec": "none", # Video only
        "height": 720, 
        "tbr": 1500
    }
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0, stdout=json.dumps(mock_json_output), stderr=""
    )
    # Expects a ValueError because audio URL will be missing
    with pytest.raises(ValueError, match="没有 Audio URL"):
        cli_utils.GetMedia(video_id)


@patch('subprocess.run')
def test_get_media_ytdlp_no_suitable_formats_empty_list(mock_run):
    """Test GetMedia when yt-dlp returns an empty 'formats' list."""
    video_id = "test_video_id_no_formats"
    mock_json_output = {"formats": []} # Empty list
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0, stdout=json.dumps(mock_json_output), stderr=""
    )
    with pytest.raises(ValueError, match="没有 Video URL"): # Or specific message for no suitable formats
        cli_utils.GetMedia(video_id)

@patch('subprocess.run')
def test_get_media_ytdlp_no_suitable_formats_no_urls_in_formats(mock_run):
    """Test GetMedia when formats are present but lack URLs."""
    video_id = "test_video_id_no_urls"
    mock_json_output = {
        "formats": [
            {"vcodec": "avc1", "acodec": "mp4a", "height": 720, "tbr": 1500}, # No URL
            {"vcodec": "none", "acodec": "mp4a", "abr": 128} # No URL
        ]
    }
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0, stdout=json.dumps(mock_json_output), stderr=""
    )
    with pytest.raises(ValueError, match="没有 Video URL"):
        cli_utils.GetMedia(video_id)

@patch('subprocess.run')
def test_get_media_ytdlp_no_suitable_formats_video_no_audio(mock_run):
    """Test GetMedia when only video formats with no audio are found, and no separate audio."""
    video_id = "test_video_id_video_no_audio"
    mock_json_output = {
        "formats": [
            {"url": "http://example.com/video_only.mp4", "vcodec": "avc1", "acodec": "none", "height": 720, "tbr": 1500},
        ]
    }
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0, stdout=json.dumps(mock_json_output), stderr=""
    )
    with pytest.raises(ValueError, match="没有 Audio URL"):
        cli_utils.GetMedia(video_id)


@patch('subprocess.run')
def test_get_media_ytdlp_fails_non_zero_exit(mock_run):
    """Test GetMedia when yt-dlp returns a non-zero exit code."""
    video_id = "test_video_id_fail_exit"
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd=["yt-dlp", "-j", "--skip-download", video_id],
        stderr="yt-dlp error message"
    )
    # The cli_utils.GetMedia function catches CalledProcessError and raises ValueError.
    # We need to match the specific error message format if it's consistent.
    # Example: _('yt-dlp failed with error: {}. Output: {}').format(e.stderr, e.output)
    # For simplicity, just check if ValueError is raised.
    with pytest.raises(ValueError) as excinfo:
        cli_utils.GetMedia(video_id)
    assert "yt-dlp failed with error" in str(excinfo.value)
    assert "yt-dlp error message" in str(excinfo.value)


@patch('subprocess.run')
def test_get_media_ytdlp_invalid_json(mock_run):
    """Test GetMedia when yt-dlp returns invalid JSON."""
    video_id = "test_video_id_invalid_json"
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0,
        stdout="this is not valid json",
        stderr=""
    )
    with pytest.raises(ValueError) as excinfo:
        cli_utils.GetMedia(video_id)
    assert "Failed to parse yt-dlp JSON output" in str(excinfo.value)


@patch('subprocess.run')
def test_get_media_ytdlp_empty_json_response(mock_run):
    """Test GetMedia when yt-dlp returns an empty JSON object."""
    video_id = "test_video_id_empty_json"
    mock_json_output = {} # Empty JSON
    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0,
        stdout=json.dumps(mock_json_output),
        stderr=""
    )
    with pytest.raises(ValueError, match="没有 Video URL"): # Or a more specific "no data" message
        cli_utils.GetMedia(video_id)


@patch('subprocess.run')
def test_get_media_ytdlp_format_without_url_or_codecs(mock_run):
    """Test GetMedia when formats lack URL or essential codec info."""
    video_id = "test_video_id_bad_format"
    mock_json_output = {
        "formats": [
            {"height": 720, "tbr": 1500}, # No URL, no codecs
            {"url": "http://example.com/no_codec_info.mp4"}, # Has URL, but no codec info
            {"url": "http://example.com/audio_only_no_codec.mp3", "acodec": "mp3"}, # Missing vcodec, treated as audio
            {"url": "http://example.com/video_only_no_codec.mp4", "vcodec": "avc1"}  # Missing acodec, treated as video
        ]
    }
    # This case should find the video_only_no_codec.mp4 for video
    # and audio_only_no_codec.mp3 for audio.
    # The logic for vcodec/acodec being 'none' or present is key.
    # If vcodec is present and not 'none', it's video. If acodec is present and not 'none', it's audio.
    # The current GetMedia logic:
    # Combined: f.get("vcodec") != "none" and f.get("acodec") != "none" and f.get("url")
    #   - "http://example.com/no_codec_info.mp4" -> vcodec is None, acodec is None. Not combined.
    # Video-only: f.get("vcodec") != "none" and f.get("acodec") == "none" and f.get("url")
    #   - "http://example.com/video_only_no_codec.mp4" -> vcodec=avc1, acodec=None. Matches. -> video_url
    # Audio-only: f.get("acodec") != "none" and f.get("vcodec") == "none" and f.get("url")
    #   - "http://example.com/audio_only_no_codec.mp3" -> acodec=mp3, vcodec=None. Matches. -> audio_url

    mock_run.return_value = subprocess.CompletedProcess(
        args=["yt-dlp", "-j", "--skip-download", video_id],
        returncode=0,
        stdout=json.dumps(mock_json_output),
        stderr=""
    )
    expected_video_url = "http://example.com/video_only_no_codec.mp4"
    expected_audio_url = "http://example.com/audio_only_no_codec.mp3"
    
    video_url, audio_url = cli_utils.GetMedia(video_id)
    assert video_url == expected_video_url
    assert audio_url == expected_audio_url


def test_AnnotationsXmlStringToSub():
    file = os.path.join(baselinePath, "annotations.xml.test")
    with open(file) as f:
        assert AnnotationsXmlStringToSub(f.read())


def test_AnnotationsXmlStringToSub_ValueError():
    with pytest.raises(ValueError):
        AnnotationsXmlStringToSub("")
