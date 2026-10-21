"""Minimal, safe survey-provider detection API for FilthyCashout."""
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="FilthyCashout Survey Helper API",
    version="0.1.0",
    description="Classifies supported survey URLs; does not open surveys or submit answers.",
)

# Set CORS_ORIGINS to comma-separated trusted origins in production.
import os
origins = [item.strip() for item in os.getenv("CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",") if item.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

PROVIDERS = {
    "qualtrics.com": "Qualtrics",
    "your-surveys.com": "Your-Surveys",
    "surveyjunkie.com": "Survey Junkie",
    "pollfish.com": "Pollfish",
}


class DetectRequest(BaseModel):
    url: str = Field(min_length=8, max_length=2048)

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        parsed = urlsplit(value.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("Provide a complete http or https URL.")
        if parsed.username or parsed.password:
            raise ValueError("URLs containing credentials are not accepted.")
        host = parsed.hostname.lower().rstrip(".")
        if host in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("Local URLs are not accepted.")
        return value.strip()


def detect_provider(url: str) -> str | None:
    host = urlsplit(url).hostname
    if not host:
        return None
    host = host.lower().rstrip(".")
    for domain, provider in PROVIDERS.items():
        if host == domain or host.endswith("." + domain):
            return provider
    return None


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "filthycashout-survey-helper"}


@app.post("/api/detect")
def detect(request: DetectRequest):
    provider = detect_provider(request.url)
    return {
        "provider": provider or "Unknown",
        "known_provider": provider is not None,
        "message": (
            "Matched the URL hostname. This does not verify the survey's legitimacy."
            if provider
            else "No supported provider matched. Check the domain carefully."
        ),
    }


@app.post("/api/suggest")
def suggest():
    raise HTTPException(
        status_code=501,
        detail=(
            "Answer suggestions are not enabled yet. A future version should use "
            "user-provided facts and require review; this API never invents profile data."
        ),
    )
