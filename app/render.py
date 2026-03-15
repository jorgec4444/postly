# Copyright © 2025 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause

"""Rendering helpers: tweet HTML generation and screenshot capture.

Uses Playwright on Linux/Mac (production) and Pillow on Windows (dev fallback).
The public API is a single coroutine: ``capture_tweet_screenshot``.
"""
import asyncio
import base64
import io
import logging
import platform
import textwrap
from datetime import datetime

logger = logging.getLogger(__name__)

IS_WINDOWS = platform.system() == "Windows"

# ── Theme definitions ─────────────────────────────────────────────────────────

_THEMES: dict[str, dict[str, str]] = {
    "light": {
        "bg": "#ffffff",
        "text": "#0f1419",
        "secondary": "#536471",
        "border": "#eff3f4",
    },
    "dark": {
        "bg": "#15202b",
        "text": "#ffffff",
        "secondary": "#8b98a5",
        "border": "#38444d",
    },
    "gradient": {
        "bg": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "text": "#ffffff",
        "secondary": "#e0e0e0",
        "border": "rgba(255,255,255,0.2)",
    },
    "sunset": {
        "bg": "linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)",
        "text": "#ffffff",
        "secondary": "#f5f5f5",
        "border": "rgba(255,255,255,0.3)",
    },
    "ocean": {
        "bg": "linear-gradient(135deg, #667eea 0%, #48dbfb 100%)",
        "text": "#ffffff",
        "secondary": "#e8f8ff",
        "border": "rgba(255,255,255,0.3)",
    },
    "forest": {
        "bg": "linear-gradient(135deg, #38ada9 0%, #78e08f 100%)",
        "text": "#ffffff",
        "secondary": "#e8f5e9",
        "border": "rgba(255,255,255,0.3)",
    },
    "fire": {
        "bg": "linear-gradient(135deg, #ee5a6f 0%, #f7b731 100%)",
        "text": "#ffffff",
        "secondary": "#fff3e0",
        "border": "rgba(255,255,255,0.3)",
    },
    "midnight": {
        "bg": "linear-gradient(135deg, #2c3e50 0%, #34495e 100%)",
        "text": "#ffffff",
        "secondary": "#bdc3c7",
        "border": "rgba(255,255,255,0.2)",
    },
}

VALID_THEMES = frozenset(_THEMES.keys())
DEFAULT_THEME = "light"


# ── HTML generation ───────────────────────────────────────────────────────────

def generate_tweet_html(text: str, theme: str = DEFAULT_THEME) -> str:
    """Return a self-contained HTML document that renders a tweet card."""
    colors = _THEMES.get(theme, _THEMES[DEFAULT_THEME])
    formatted_text = text.replace("\n", "<br>")
    timestamp = datetime.now().strftime("%I:%M %p · %b %d, %Y")

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: {colors['bg']};
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 40px;
    }}
    .card {{
      background: {colors['bg']};
      border: 2px solid {colors['border']};
      border-radius: 16px;
      padding: 32px;
      max-width: 600px;
      width: 100%;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }}
    .header {{ display: flex; align-items: center; margin-bottom: 16px; }}
    .avatar {{
      width: 48px; height: 48px; border-radius: 50%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      margin-right: 12px; flex-shrink: 0;
    }}
    .name {{ font-weight: 700; font-size: 16px; color: {colors['text']}; }}
    .handle {{ color: {colors['secondary']}; font-size: 15px; }}
    .content {{
      font-size: 20px; line-height: 1.5;
      color: {colors['text']}; margin-bottom: 16px; word-wrap: break-word;
    }}
    .footer {{
      color: {colors['secondary']}; font-size: 14px;
      padding-top: 16px; border-top: 1px solid {colors['border']};
    }}
    .watermark {{
      text-align: center; margin-top: 24px; padding-top: 16px;
      border-top: 1px solid {colors['border']};
      color: {colors['secondary']}; font-size: 12px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="avatar"></div>
      <div>
        <div class="name">TweetCraft User</div>
        <div class="handle">@tweetcraft</div>
      </div>
    </div>
    <div class="content">{formatted_text}</div>
    <div class="footer">{timestamp}</div>
    <div class="watermark">🎨 Created with TweetCraft AI</div>
  </div>
</body>
</html>"""


# ── Screenshot capture ────────────────────────────────────────────────────────

async def _capture_playwright(html: str) -> str:
    """Capture a real screenshot using Playwright (Linux / Mac)."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page(viewport={"width": 800, "height": 600})
            await page.set_content(html, wait_until="networkidle")
            screenshot = await page.screenshot(type="png", full_page=True)
        finally:
            await browser.close()

    return base64.b64encode(screenshot).decode("utf-8")


async def _capture_pillow(text: str) -> str:
    """Generate a simple tweet image using Pillow (Windows dev fallback)."""
    from PIL import Image, ImageDraw, ImageFont

    logger.warning("Using Pillow fallback (Windows dev mode). Production uses Playwright.")

    img = Image.new("RGB", (800, 600), color="#ffffff")
    draw = ImageDraw.Draw(img)

    # Card border
    draw.rectangle([40, 40, 760, 560], outline="#e5e7eb", width=2)
    # Avatar
    draw.ellipse([60, 60, 110, 110], fill="#667eea")

    try:
        font_name = ImageFont.truetype("arial.ttf", 16)
        font_handle = ImageFont.truetype("arial.ttf", 14)
        font_text = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except OSError:
        font_name = font_handle = font_text = font_small = ImageFont.load_default()

    draw.text((130, 65), "TweetCraft User", fill="#0f1419", font=font_name)
    draw.text((130, 90), "@tweetcraft", fill="#536471", font=font_handle)

    y = 130
    for paragraph in text.split("\n"):
        for line in textwrap.wrap(paragraph, width=60) or [""]:
            if y > 490:
                break
            draw.text((60, y), line, fill="#0f1419", font=font_text)
            y += 30

    draw.text(
        (60, 520),
        "Preview mode — production renders real HTML",
        fill="#9ca3af",
        font=font_small,
    )
    draw.text((300, 550), "🎨 Created with TweetCraft AI", fill="#667eea", font=font_small)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


async def capture_tweet_screenshot(html: str, text: str = "") -> str:
    """Unified async entry point — picks the right backend automatically.

    Args:
        html:  HTML string produced by ``generate_tweet_html``.
        text:  Plain tweet text (only used by the Pillow fallback).

    Returns:
        Base64-encoded PNG string.
    """
    if IS_WINDOWS:
        return await _capture_pillow(text)
    return await _capture_playwright(html)
