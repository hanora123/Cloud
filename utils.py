#!/usr/bin/env python3

import os
import subprocess
import platform

def check_dependencies():
    """Check if required dependencies are installed."""
    missing_deps = []
    
    # Check for QEMU
    try:
        subprocess.run(["qemu-img", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing_deps.append("QEMU")
    
    # Check for Docker
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing_deps.append("Docker")
    
    return missing_deps

def get_system_info():
    """Get system information."""
    system_info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version()
    }
    
    return system_info

def format_size(size_bytes):
    """Format size in bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"