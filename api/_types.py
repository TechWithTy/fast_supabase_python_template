supabase_types = [
    "AsyncSupabaseAuthClient",
    "AsyncClient",
    "AsyncClientOptions",
    "AsyncSupabaseStorageClient",
    "SupabaseAuthClient",
    "Client",
    "ClientOptions",
    "SupabaseStorageClient",
    "PostgrestAPIError",
    "PostgrestAPIResponse",
    "StorageException",
    "AuthApiError",
    "AuthError",
    "AuthImplicitGrantRedirectError",
    "AuthInvalidCredentialsError",
    "AuthRetryableError",
    "AuthSessionMissingError",
    "AuthWeakPasswordError",
    "AuthUnknownError",
    "FunctionsHttpError",
    "FunctionsRelayError",
    "FunctionsError",
    "AuthorizationError",
    "NotConnectedError",
]


class TypesConfig:
    import_method = "from app.core.third_party_integrations.supabase_home._client"
    conversion_method = "camel_case"
    library_name = "app.core.third_party_integrations.supabase_home"
    relative_file_path = (
        "backend/app/core/third_party_integrations/supabase_home/api/_schema.py"
    )
    absolute_file_path = "C:\\Users\\{user}\\Documents\\Github\\lead_ignite_backend_3.0\\backend\\app\\core\\third_party_integrations\\supabase_home\\api\\_schema.py"
    types = supabase_types
