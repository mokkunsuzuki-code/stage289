from __future__ import annotations

import json
import os
import subprocess
import tempfile
from typing import Any


def stable_json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def gpg_clearsign_text(payload_text: str) -> tuple[str | None, str | None]:
    """
    Sign text using local GPG.
    Returns: (signed_text, error_message)
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "payload.json")
            output_path = input_path + ".asc"

            with open(input_path, "w", encoding="utf-8") as f:
                f.write(payload_text)

            cmd = [
                "gpg",
                "--yes",
                "--armor",
                "--output",
                output_path,
                "--clearsign",
                input_path,
            ]
            completed = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
            )

            if completed.returncode != 0:
                stderr = completed.stderr.strip() or completed.stdout.strip()
                return None, f"GPG signing failed: {stderr}"

            with open(output_path, "r", encoding="utf-8") as f:
                signed_text = f.read()

            return signed_text, None

    except FileNotFoundError:
        return None, "GPG not found on this machine."
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def sign_result(result: dict[str, Any]) -> tuple[str | None, str | None]:
    payload_text = stable_json_dumps(result)
    return gpg_clearsign_text(payload_text)
