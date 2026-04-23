# Stage289: Verification API

## Overview

Stage289 introduces a minimal Verification API for QSP / VEP.

This stage turns verification into an external API interface.

Clients can submit:
- a public URL
- a manifest object

The API returns:
- verification decision
- trust score
- evidence
- GPG signature of the result

This is the first API-shaped stage that can later evolve into:
- SaaS
- public verification service
- OpenSSF-compatible verification endpoint
- hardware-backed signing with YubiKey

---

## API

### Health check

GET /

Response example:

```json
{
  "stage": "289",
  "name": "Verification API",
  "status": "ok"
}
Verification

POST /verify

Request example:

{
  "url": "https://example.com",
  "manifest": {
    "execution": true,
    "identity": true,
    "timestamp": true,
    "workflow": "github-actions"
  }
}

Response fields:

decision
reason
trust_score
breakdown
evidence
signature
signature_error
Local run
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000/
http://127.0.0.1:8000/docs
Design

Current signing:

local GPG software key

Future upgrade:

YubiKey-backed signing
same API surface, stronger trust

This means Stage289 is already functional now,
while the signing backend can later be upgraded without changing the API contract.

Trust model (minimal initial version)
Integrity
Execution
Identity
Time

Current decision thresholds:

accept: trust_score >= 0.85
pending: 0.45 <= trust_score < 0.85
reject: trust_score < 0.45
Why this stage matters

Previous stages established:

evidence
verification
public exposure
trust scoring

Stage289 adds:

API form
machine-readable verification interface
external integration path

This is the step from:

verification page
to:
verification service
License

MIT License
