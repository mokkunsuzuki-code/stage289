# Stage289: Verification API

## Overview

Stage289 introduces a public Verification API for QSP / VEP.

Clients can submit:
- a public URL
- a manifest object

The API returns:
- verification decision
- trust score
- evidence

This stage converts verification into a machine-readable API.

---

## Public API

Base URL:

https://stage289.onrender.com

Endpoint:

POST /verify

Example:

```bash
curl -X POST "https://stage289.onrender.com/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "manifest": {
      "execution": true,
      "identity": true,
      "timestamp": true,
      "workflow": "github-actions"
    }
  }'
Response
decision
reason
trust_score
breakdown
evidence
signature
signature_error
Public deployment note

The public Render deployment exposes the verification API externally.

At this stage:

Verification (decision, trust score, evidence) is fully available
The API is publicly accessible

GPG signing is currently available in the local environment only.

The public deployment does not include a server-side secret key, therefore:

signature may be null
signature_error may indicate that no secret key is installed

This is intentional for security reasons.

Trust Model
Integrity
Execution
Identity
Time

Decision thresholds:

accept: trust_score >= 0.85
pending: 0.45 <= trust_score < 0.85
reject: trust_score < 0.45
Roadmap

Next stage:

Hardware-backed signing (YubiKey)
Stronger identity trust
Production-grade signing architecture
License

MIT License