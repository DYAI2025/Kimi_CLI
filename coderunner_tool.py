import json
import subprocess
import tempfile
from typing import Dict


def run_code(language: str, code: str, timeout: int = 10) -> Dict[str, str]:
    """Execute code safely in a subprocess and return the result."""
    if language not in {"python", "javascript"}:
        raise ValueError("Unsupported language")

    if language == "python":
        cmd = ["python3", "-I", "-"]
    else:  # javascript
        cmd = ["node", "--input-type=module", "-"]

    try:
        proc = subprocess.run(
            cmd,
            input=code.encode(),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "stdout": proc.stdout[:1000],
            "stderr": proc.stderr[:1000],
            "exit_code": proc.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Execution timed out", "exit_code": -1}
    except Exception as exc:
        return {"stdout": "", "stderr": str(exc), "exit_code": -1}
