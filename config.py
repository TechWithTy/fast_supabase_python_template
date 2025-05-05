from pydantic import BaseModel, Field

from app.core.config import settings


class SupabaseConfig(BaseModel):
    """
    Configuration for Supabase integration.
    Pulls from main settings.database and allows for extension with integration-specific options.
    """

    url: str = Field(default_factory=lambda: settings.database.SUPABASE_URL)
    anon_key: str = Field(default_factory=lambda: settings.database.SUPABASE_ANON_KEY)
    service_role_key: str = Field(
        default_factory=lambda: settings.database.SUPABASE_SERVICE_ROLE_KEY
    )
    jwt_secret: str = Field(
        default_factory=lambda: settings.database.SUPABASE_JWT_SECRET
    )

    timeout: int = Field(
        default=30, description="Default HTTP timeout for Supabase requests (seconds)"
    )
    retry_attempts: int = Field(
        default=3, description="Number of retry attempts for failed Supabase requests"
    )
    enable_logging: bool = Field(
        default=True, description="Enable detailed logging for Supabase integration"
    )
    # * Add more advanced or project-specific options as needed

    model_config = {"arbitrary_types_allowed": True}


supabase_config = SupabaseConfig()
