from __future__ import annotations

import hashlib
import json
from typing import Any


def stable_json_dumps(data: Any) -> str:
    """Deterministic JSON string for hashing/signing."""
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def sha256_hex_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_hex_text(text: str) -> str:
    return sha256_hex_bytes(text.encode("utf-8"))


def fetch_url_text(url: str, timeout: int = 10) -> tuple[str | None, str | None]:
    """
    Try to fetch the URL content.
    Returns: (text, error_message)
    """
    try:
        import requests

        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text, None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def verify_input(url: str | None, manifest: dict[str, Any] | None) -> dict[str, Any]:
    """
    Minimal Stage289 verification model.

    Scoring model (simple initial version):
    - integrity: 1.0 if manifest exists, else 0.0
    - execution: 1.0 if manifest contains execution/ci hints, else 0.25
    - identity: 1.0 if manifest contains identity/signature hints, else 0.25
    - time: 1.0 if manifest contains ots/timestamp hints, else 0.25

    decision:
    - accept  : trust_score >= 0.85
    - pending : 0.45 <= trust_score < 0.85
    - reject  : trust_score < 0.45
    """
    manifest = manifest or {}
    evidence: dict[str, Any] = {}

    manifest_text = stable_json_dumps(manifest)
    evidence["manifest_sha256"] = sha256_hex_text(manifest_text)
    evidence["manifest_present"] = bool(manifest)

    fetched_url_text: str | None = None
    url_fetch_error: str | None = None

    if url:
        fetched_url_text, url_fetch_error = fetch_url_text(url)
        evidence["url"] = url
        evidence["url_fetch_ok"] = fetched_url_text is not None
        if fetched_url_text is not None:
            evidence["url_sha256"] = sha256_hex_text(fetched_url_text)
        if url_fetch_error:
            evidence["url_fetch_error"] = url_fetch_error
    else:
        evidence["url"] = None
        evidence["url_fetch_ok"] = False

    integrity = 1.0 if manifest else 0.0

    execution = 0.25
    if any(key in manifest for key in ["execution", "ci", "workflow", "github_actions_receipt"]):
        execution = 1.0

    identity = 0.25
    if any(key in manifest for key in ["identity", "signature", "public_key", "signer"]):
        identity = 1.0

    time_trust = 0.25
    if any(key in manifest for key in ["ots", "timestamp", "time_trust", "bitcoin_anchor"]):
        time_trust = 1.0

    trust_score = round((integrity + execution + identity + time_trust) / 4.0, 3)

    if trust_score >= 0.85:
        decision = "accept"
        reason = "All major trust components are present."
    elif trust_score >= 0.45:
        decision = "pending"
        reason = "Some trust components are missing or incomplete."
    else:
        decision = "reject"
        reason = "Trust evidence is too incomplete."

    result = {
        "decision": decision,
        "reason": reason,
        "trust_score": trust_score,
        "breakdown": {
            "integrity": integrity,
            "execution": execution,
            "identity": identity,
            "time": time_trust,
        },
        "evidence": evidence,
    }

    return result
