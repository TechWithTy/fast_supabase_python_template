from .client import get_supabase_client
from .sdk.auth import SupabaseAuthService
from .sdk.database import SupabaseDatabaseService
from .sdk.edge_functions import SupabaseEdgeFunctionsService
from .sdk.realtime import SupabaseRealtimeService
from .sdk.storage import SupabaseStorageService


class SupabaseClient:
    """
    Client for interacting with all Supabase services.

    This class provides a unified interface to access all Supabase services:
    - Auth
    - Database
    - Storage
    - Edge Functions
    - Realtime
    """

    def __init__(self, client):
        # Initialize the raw supabase client
        self._raw_client = client

        # Initialize service classes
        self.auth = SupabaseAuthService(client)
        self.database = SupabaseDatabaseService(client)
        self.storage = SupabaseStorageService(client)
        self.edge_functions = SupabaseEdgeFunctionsService(client)
        self.realtime = SupabaseRealtimeService(client)

    @classmethod
    async def create(cls):
        client = await get_supabase_client()
        return cls(client)

    def get_auth_service(self) -> SupabaseAuthService:
        """
        Get the Auth service.

        Returns:
            SupabaseAuthService instance
        """
        return self.auth

    def get_database_service(self) -> SupabaseDatabaseService:
        """
        Get the Database service.

        Returns:
            SupabaseDatabaseService instance
        """
        return self.database

    def get_storage_service(self) -> SupabaseStorageService:
        """
        Get the Storage service.

        Returns:
            SupabaseStorageService instance
        """
        return self.storage

    def get_edge_functions_service(self) -> SupabaseEdgeFunctionsService:
        """
        Get the Edge Functions service.

        Returns:
            SupabaseEdgeFunctionsService instance
        """
        return self.edge_functions

    def get_realtime_service(self) -> SupabaseRealtimeService:
        """
        Get the Realtime service.

        Returns:
            SupabaseRealtimeService instance
        """
        return self.realtime

    def get_raw_client(self):
        """
        Get the raw Supabase client from supabase-py.

        This provides direct access to the underlying client if needed for
        advanced operations not covered by the service classes.

        Returns:
            supabase.Client instance
        """
        return self._raw_client



