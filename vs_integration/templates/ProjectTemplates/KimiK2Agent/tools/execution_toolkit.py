#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Execution Toolkit for Kimi K2 Agent
Safe and controlled execution of shell commands and file operations
"""

import os
import subprocess
import tempfile
from typing import Dict, Optional
from pathlib import Path


def execute_shell_command(command: str, timeout: int = 30, cwd: Optional[str] = None) -> Dict[str, str]:
    """
    Execute a shell command safely with timeout and capture output
    
    Args:
        command: Command to execute
        timeout: Timeout in seconds
        cwd: Working directory
        
    Returns:
        Dictionary with stdout, stderr, and exit_code
    """
    try:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        return {
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "exit_code": proc.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds",
            "exit_code": -1
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Execution error: {str(e)}",
            "exit_code": -1
        }


def read_file(path: str, encoding: str = 'utf-8') -> str:
    """
    Read a file and return its contents
    
    Args:
        path: File path
        encoding: File encoding
        
    Returns:
        File contents
    """
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Error reading file {path}: {e}")


def write_file(path: str, content: str, encoding: str = 'utf-8') -> None:
    """
    Write content to a file, creating directories if necessary
    
    Args:
        path: File path
        content: Content to write
        encoding: File encoding
    """
    try:
        # Create parent directories if they don't exist
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"Error writing file {path}: {e}")


def delete_file(path: str) -> bool:
    """
    Delete a file if it exists
    
    Args:
        path: File path
        
    Returns:
        True if file was deleted or didn't exist, False on error
    """
    try:
        if os.path.exists(path):
            os.remove(path)
        return True
    except Exception as e:
        print(f"Error deleting file {path}: {e}")
        return False


def list_files(directory: str, pattern: str = "*") -> list:
    """
    List files in a directory matching a pattern
    
    Args:
        directory: Directory path
        pattern: File pattern (glob)
        
    Returns:
        List of matching file paths
    """
    try:
        path = Path(directory)
        return [str(p) for p in path.glob(pattern) if p.is_file()]
    except Exception as e:
        print(f"Error listing files in {directory}: {e}")
        return []


def create_temp_file(content: str, suffix: str = ".txt") -> str:
    """
    Create a temporary file with content
    
    Args:
        content: File content
        suffix: File suffix
        
    Returns:
        Path to temporary file
    """
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as tmp:
            tmp.write(content)
            return tmp.name
    except Exception as e:
        raise IOError(f"Error creating temporary file: {e}")


def get_file_info(path: str) -> Dict[str, any]:
    """
    Get information about a file
    
    Args:
        path: File path
        
    Returns:
        Dictionary with file information
    """
    try:
        stat = os.stat(path)
        return {
            "exists": True,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "created": stat.st_ctime,
            "is_file": os.path.isfile(path),
            "is_dir": os.path.isdir(path),
            "extension": Path(path).suffix,
            "name": Path(path).name
        }
    except Exception as e:
        return {"exists": False, "error": str(e)}


def safe_command_check(command: str) -> bool:
    """
    Check if a command is safe to execute
    
    Args:
        command: Command to check
        
    Returns:
        True if command is considered safe
    """
    # List of dangerous commands/patterns
    dangerous_patterns = [
        'rm -rf /',
        'format',
        'fdisk',
        'dd if=',
        '> /dev/',
        'chmod 777',
        'curl | bash',
        'wget | bash',
        'sudo rm',
        'del /f /q',
        'rmdir /s'
    ]
    
    command_lower = command.lower()
    return not any(pattern in command_lower for pattern in dangerous_patterns)