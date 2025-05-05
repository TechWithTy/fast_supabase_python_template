# Re-export SupabaseService from app.py for compatibility with tests and usage
from ._service import SupabaseService as SupabaseService_insecure
from .app import SupabaseClient

__all__ = [
    "SupabaseClient",
    "SupabaseService_insecure",
]
