# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause

"""Postly — FastAPI application entry point."""
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import ADMIN_API_KEY, init_openai_client
from app.database import init_supabase

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s: %(message)s")
logger = logging.getLogger(__name__)


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    logger.info("Starting Postly`…")
    init_supabase()
    init_openai_client()
    logger.info("Startup complete.")
    yield
    logger.info("Shutting down.")


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Orkly",
    description="Orchestrate your content, and more with AI.",
    version="2.0.0",
    contact={"name": "Jorge Vinagre", "email": "jorgecdev444@gmail.com"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://postly.vinagre444.workers.dev"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["meta"])
async def root():
    return {
        "service": "Orkly",
        "version": "2.0.0",
        "endpoints": {
            "POST /improve": "Improve a text with AI (3 variations)",
            "GET  /rate-limit/status": "Check remaining free generations",
            "POST /feedback": "Submit feedback",
            "GET  /health": "Health check",
            "GET  /admin/stats": "Admin statistics (requires API key)",
        },
    }


@app.get("/health", tags=["meta"])
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/admin/stats", tags=["admin"])
async def admin_stats(api_key: str | None = None):
    """Aggregated usage statistics (protected by ADMIN_API_KEY)."""
    if not ADMIN_API_KEY or api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return rate_limiter.get_stats()
