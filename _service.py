import logging
from typing import Any

import httpx
from fastapi import HTTPException
from supabase._async.client import AsyncClient as Client
from supabase._async.client import create_client

from app.core.third_party_integrations.supabase_home.config import supabase_config
from app.core.third_party_integrations.supabase_home.exceptions.index import (
    SupabaseAuthError,
)

logger = logging.getLogger("apps.supabase_home")


class SupabaseUnsecureService:
    """
    Service class for interacting with Supabase API.

    This class provides methods for interacting with various Supabase services:
    - Auth (user management)
    - Database (PostgreSQL)
    - Storage
    - Edge Functions
    - Realtime

    It handles authentication, request formatting, and response parsing.
    """

    def __init__(self):
        self.base_url = supabase_config.url
        self.anon_key = supabase_config.anon_key
        self.service_role_key = supabase_config.service_role_key
        self.raw = self._get_service_role_supabase_client()

        self._configure_service()

        if not self.base_url:
            logger.error("SUPABASE_URL is not set in settings")
            raise ValueError("SUPABASE_URL is not set in settings")

        if not self.anon_key:
            logger.error("SUPABASE_ANON_KEY is not set in settings")
            raise ValueError("SUPABASE_ANON_KEY is not set in settings")

        if not self.service_role_key:
            logger.warning(
                "SUPABASE_SERVICE_ROLE_KEY is not set in settings. Admin operations will not work."
            )

    def _get_service_role_supabase_client(self) -> Client:
        """
        Create a Supabase client using the service role key (bypasses RLS, for admin ops).
        Returns:
            An instance of the Supabase AsyncClient with service role privileges.
        """
        if not self.base_url or not self.service_role_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required.")
        return create_client(self.base_url, self.service_role_key)

    def _get_headers(
        self, auth_token: str | None, is_admin: bool = False
    ) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "apikey": self.service_role_key if is_admin else self.anon_key,
        }

        if is_admin:
            if not self.service_role_key:
                raise SupabaseAuthError(
                    "Service role key is required for admin operations"
                )
            headers["Authorization"] = f"Bearer {self.service_role_key}"
        elif auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        return headers

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        auth_token: str | None,
        is_admin: bool = False,
        data: dict[str, Any] | None,
        params: dict[str, Any] | None,
        headers: dict[str, str] | None,
        timeout: int = 30,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"

        request_headers = self._get_headers(auth_token, is_admin)
        if headers:
            request_headers.update(headers)

        logger.info(f"Making {method} request to {url}")
        logger.info(f"Headers: {request_headers}")
        if "Authorization" in request_headers:
            auth_header = request_headers["Authorization"]
            logger.info(f"Authorization header: {auth_header[:15]}...")
        else:
            logger.info("No Authorization header found")

        logger.info(f"Request data: {data}")
        logger.info(f"Request params: {params}")

        if (
            data is None
            and "Content-Type" in request_headers
            and request_headers["Content-Type"] == "application/json"
        ):
            data = {}
            logger.info("Initialized empty JSON data")

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    json=data,
                    params=params,
                )

            logger.info(f"Request to {url}: {method} - Status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")

            try:
                if response.content:
                    logger.info(f"Response content: {response.content[:200]}...")
                    if response.status_code >= 400:
                        logger.error(f"Error response: {response.content}")
            except Exception as e:
                logger.error(f"Error logging response content: {str(e)}")

            if response.status_code == 401 or response.status_code == 403:
                error_detail = self._parse_error_response(response)
                logger.error(f"Authentication error: {error_detail}")
                raise HTTPException(
                    status_code=response.status_code, detail=str(error_detail)
                )

            response.raise_for_status()

            if response.content:
                return response.json()
            return {}

        except httpx.HTTPStatusError as e:
            error_detail = self._parse_error_response(e.response)
            logger.error(f"Supabase API error: {str(e)} - Details: {error_detail}")
            raise HTTPException(
                status_code=e.response.status_code, detail=str(error_detail)
            )

        except httpx.RequestError as e:
            logger.error(f"Supabase request exception: {str(e)}")
            raise HTTPException(status_code=500, detail="Request error")

        except Exception as e:
            logger.exception(f"Unexpected error during Supabase request: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Unexpected error during Supabase request"
            )

    def _parse_error_response(self, response) -> dict:
        try:
            return response.json()
        except Exception:
            return {
                "status": getattr(response, "status_code", None),
                "message": getattr(response, "text", str(response)),
            }
