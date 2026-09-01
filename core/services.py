"""
Shared core service utilities.
"""
from typing import Dict, Any


def get_system_health() -> Dict[str, Any]:
    """Returns system status and configuration summary."""
    return {
        "status": "healthy",
        "service": "resumeforge-api",
        "version": "1.0.0"
    }
