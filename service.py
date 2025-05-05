# Re-export SupabaseService from app.py for compatibility with tests and usage
from ._service import SupabaseUnsecureService
from .app import SupabaseClient

__all__ = [
    "SupabaseClient",
    "SupabaseUnsecureService",
]
