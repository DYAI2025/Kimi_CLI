import os
import subprocess
from typing import Dict


def read_file(path: str) -> str:
    """Read a file and return its contents."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    """Write content to a file, creating it if necessary."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def delete_file(path: str) -> None:
    """Delete a file if it exists."""
    if os.path.exists(path):
        os.remove(path)


def execute_shell_command(command: str, timeout: int = 30) -> Dict[str, str]:
    """Execute an arbitrary shell command and capture output."""
    try:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "exit_code": proc.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Execution timed out", "exit_code": -1}
