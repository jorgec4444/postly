# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause

"""Central configuration and shared clients.
Reads environment variables, validates them at startup, and initialises
the OpenAI client lazily so unit tests can patch it without side-effects.
"""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load .env from the project root (one level above /app)
_env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(_env_path)

# ── OpenAI ──────────────────────────────────────────────────────────────────
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

# Correct model name is "gpt-4o-mini"
MODEL_NAME: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ── Supabase ─────────────────────────────────────────────────────────────────
SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")

# ── R2 Storage (Cloudflare) ─────────────────────────────────────────────────
R2_ACCESS_KEY_ID: Optional[str] = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY: Optional[str] = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME: Optional[str] = os.getenv("R2_BUCKET_NAME")
R2_ENDPOINT: Optional[str] = os.getenv("R2_ENDPOINT")

# ── R2 Storage public logos bucket (Cloudflare) ─────────────────────────────────────────────────

R2_LOGOS_BUCKET_NAME = os.getenv("R2_LOGOS_BUCKET_NAME", "orkly-logos")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "")

# ── Admin ─────────────────────────────────────────────────────────────────────
ADMIN_API_KEY: Optional[str] = os.getenv("ADMIN_API_KEY")

# ── Rate limiting ─────────────────────────────────────────────────────────────
def _parse_int_env(name: str, default: int) -> int:
    """Parse an integer env-var safely; fall back to *default* instead of crashing."""
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        print(f"[config] WARNING: {name}={raw!r} is not a valid integer — using default {default}")
        return default

FREE_DAILY_LIMIT: int = _parse_int_env("MAX_FREE_GENERATIONS_PER_DAY", 5)
LOGGED_DAILY_LIMIT: int = _parse_int_env("MAX_LOGGED_GENERATIONS_PER_DAY", 15)

# ── OpenAI client (module-level singleton) ────────────────────────────────────
_openai_client = None

def init_openai_client():
    """Initialise and cache the OpenAI client. Safe to call multiple times."""
    global _openai_client
    if _openai_client is not None:
        return _openai_client

    if not OPENAI_API_KEY:
        print("[config] OpenAI client NOT initialised — OPENAI_API_KEY is missing.")
        return None

    try:
        from openai import OpenAI  # imported here so tests can mock before import
        _openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print(f"[config] OpenAI client initialised (model={MODEL_NAME}).")
        return _openai_client
    except Exception as exc:
        print(f"[config] ERROR initialising OpenAI client: {exc}")
        return None


def get_openai_client():
    """Return the cached OpenAI client, or None if unavailable."""
    return _openai_client

# ── R2 client (module-level singleton) ────────────────────────────────────
_r2_client = None

def init_r2_client():
    """Initialise and cache the R2 client. Safe to call multiple times."""
    global _r2_client
    if _r2_client is not None:
        return _r2_client
    
    if not all([R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT, R2_BUCKET_NAME]):
        print("[config] R2 client NOT initialised — missing one or more R2_* env vars.")
        return None
    try:
        import boto3
        _r2_client = boto3.client(
            "s3",
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            region_name="auto",  # R2 ignores region but boto3 requires it
        )
        print(f"[config] R2 client initialised (bucket={R2_BUCKET_NAME}).")
        return _r2_client
    except Exception as exc:
        print(f"[config] ERROR initialising R2 client: {exc}")
        return None


def get_r2_client():
    """Return the cached R2 client, or None if unavailable."""
    if _r2_client is None:
        return init_r2_client()
    return _r2_client

_r2_logos_client = None

def init_r2_logos_client():
    """Initialise and cache the R2 logos client. Safe to call multiple times."""
    global _r2_logos_client
    if _r2_logos_client is not None:
        return _r2_logos_client

    if not all([R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT, R2_LOGOS_BUCKET_NAME]):
        print("[config] R2 logos client NOT initialised — missing one or more R2_* env vars.")
        return None
    try:
        import boto3
        _r2_logos_client = boto3.client(
            "s3",
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            region_name="auto",
        )
        print(f"[config] R2 logos client initialised (bucket={R2_LOGOS_BUCKET_NAME}).")
        return _r2_logos_client
    except Exception as exc:
        print(f"[config] ERROR initialising R2 logos client: {exc}")
        return None


def get_r2_logos_client():
    """Return the cached R2 logos client, or None if unavailable."""
    if _r2_logos_client is None:
        return init_r2_logos_client()
    return _r2_logos_client