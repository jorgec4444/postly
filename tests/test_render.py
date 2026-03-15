"""Unit tests for app.render."""
import base64
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.render import DEFAULT_THEME, VALID_THEMES, generate_tweet_html


class TestGenerateTweetHtml:
    def test_contains_text(self):
        html = generate_tweet_html("Hello world")
        assert "Hello world" in html

    def test_newlines_become_br(self):
        html = generate_tweet_html("line1\nline2")
        assert "<br>" in html

    def test_valid_themes_do_not_raise(self):
        for theme in VALID_THEMES:
            html = generate_tweet_html("test", theme)
            assert "TweetCraft" in html

    def test_unknown_theme_falls_back_to_light(self):
        light_html = generate_tweet_html("test", DEFAULT_THEME)
        unknown_html = generate_tweet_html("test", "nonexistent_theme")
        # Both should contain the light theme background colour
        assert "#ffffff" in light_html
        assert "#ffffff" in unknown_html

    def test_html_is_complete_document(self):
        html = generate_tweet_html("hi")
        assert "<!DOCTYPE html>" in html
        assert "</html>" in html


class TestCaptureScreenshot:
    @pytest.mark.asyncio
    async def test_playwright_path_on_linux(self):
        """On non-Windows, should call the Playwright capture function."""
        fake_b64 = base64.b64encode(b"fake-png").decode()

        with (
            patch("app.render.IS_WINDOWS", False),
            patch("app.render._capture_playwright", new=AsyncMock(return_value=fake_b64)) as mock_pw,
        ):
            from app.render import capture_tweet_screenshot
            result = await capture_tweet_screenshot("<html/>", "test text")

        mock_pw.assert_awaited_once_with("<html/>")
        assert result == fake_b64

    @pytest.mark.asyncio
    async def test_pillow_path_on_windows(self):
        """On Windows, should call the Pillow capture function."""
        fake_b64 = base64.b64encode(b"fake-png").decode()

        with (
            patch("app.render.IS_WINDOWS", True),
            patch("app.render._capture_pillow", new=AsyncMock(return_value=fake_b64)) as mock_pillow,
        ):
            from app.render import capture_tweet_screenshot
            result = await capture_tweet_screenshot("<html/>", "test text")

        mock_pillow.assert_awaited_once_with("test text")
        assert result == fake_b64
