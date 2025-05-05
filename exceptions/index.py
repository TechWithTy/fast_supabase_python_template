class SupabaseError(Exception):
    """Base exception for Supabase-related errors"""

    pass


class SupabaseAuthError(SupabaseError):
    """Exception raised for authentication errors"""

    pass


class SupabaseAPIError(SupabaseError):
    """Exception raised for API errors"""

    def __init__(self, message: str, status_code: int = None, details: dict = None):
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)
