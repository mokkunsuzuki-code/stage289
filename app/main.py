from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.signer import sign_result
from app.verifier import verify_input


app = FastAPI(
    title="Stage289 Verification API",
    description="Minimal Verification API for QSP/VEP public verification.",
    version="289.0.0",
)


class VerifyRequest(BaseModel):
    url: str | None = Field(default=None, description="Public URL to fetch and hash")
    manifest: dict[str, Any] | None = Field(
        default=None,
        description="Verification manifest JSON object",
    )


class VerifyResponse(BaseModel):
    decision: str
    reason: str
    trust_score: float
    breakdown: dict[str, float]
    evidence: dict[str, Any]
    signature: str | None = None
    signature_error: str | None = None


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "stage": "289",
        "name": "Verification API",
        "status": "ok",
    }


@app.post("/verify", response_model=VerifyResponse)
def verify(req: VerifyRequest) -> dict[str, Any]:
    result = verify_input(url=req.url, manifest=req.manifest)
    signature, signature_error = sign_result(result)

    result["signature"] = signature
    result["signature_error"] = signature_error
    return result
