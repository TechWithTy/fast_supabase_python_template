from typing import Any

from supafunc.errors import FunctionsHttpError, FunctionsRelayError

from app.core.third_party_integrations.supabase_home._client import get_supabase_client


class SupabaseEdgeFunctionsService:
    """
    Service for invoking Supabase Edge Functions using the unified SDK client.
    Only the invoke_function method is supported, matching the official SDK.
    """

    def __init__(self):
        self.client = get_supabase_client()
        self.functions = getattr(self.client, "functions", None)

    def invoke_function(
        self,
        function_name: str,
        body: Any = None,
        headers: dict[str, str] | None,
        auth_token: str | None,
        method: str = "POST",
    ) -> Any:
        """
        Invoke a Supabase Edge Function using the official SDK.

        Args:
            function_name: Name of the function to invoke
            body: Payload to send (will be auto-serialized as JSON unless Content-Type is set)
            headers: Optional HTTP headers (must include Authorization)
            auth_token: Optional JWT for Authorization header (if not set in headers)
            method: HTTP method to use (default POST)

        Returns:
            Function response
        """
        if not self.functions or not hasattr(self.functions, "invoke"):
            raise NotImplementedError("Edge Functions SDK client is not available in this SDK version.")

        # Ensure Authorization header is present
        request_headers = headers.copy() if headers else {}
        if auth_token:
            request_headers.setdefault("Authorization", f"Bearer {auth_token}")
        elif "Authorization" not in request_headers:
            raise ValueError("Authorization header or auth_token is required for Edge Function invocation.")

        # SDK handles Content-Type and serialization automatically
        try:
            return self.functions.invoke(
                function_name,
                invoke_options={
                    "body": body,
                    "headers": request_headers,
                    "method": method,
                },
            )
        except FunctionsHttpError as exception:
            err = exception.to_dict()
            # ! Function returned an error (e.g., 4xx/5xx)
            raise RuntimeError(f'Function returned an error: {err.get("message")}', err)
        except FunctionsRelayError as exception:
            err = exception.to_dict()
            # ! Relay (Supabase infra) error
            raise RuntimeError(f'Relay error: {err.get("message")}', err)
