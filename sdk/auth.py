from typing import Any

from .._client import get_supabase_client  # ! Use the unified client


class SupabaseAuthService:
    """
    Service for interacting with Supabase Auth API using official supabase-py SDK.
    Provides methods for user management, authentication, session handling, MFA, and admin operations.
    Grouped by logical domains (Admin, MFA, Auth, Session).
    """
    def __init__(self, client: Any):
        self.client = client
        self.auth = self.client.auth
        self.auth.admin = getattr(self.auth, "admin", None)
        self.mfa = getattr(self.auth, "mfa", None)
        # Nested service classes
        self.admin = self.Admin(self.auth)
        self.mfa_service = self.MFA(self.auth)
        self.session = self.Session(self.auth)
        self.user = self.User(self.auth)

    @classmethod
    async def create(cls):
        client = await get_supabase_client()
        return cls(client)

    class Admin:
        def __init__(self, auth):
            self.admin = getattr(auth, "admin", None)

        def get_user_by_id(self, user_id: str) -> Any:
            if not self.admin:
                raise NotImplementedError("Admin user retrieval not available in SDK")
            return self.admin.get_user_by_id(user_id)

        def list_users(self, params: dict[str, Any] | None = None) -> Any:
            if not self.admin:
                raise NotImplementedError("Admin user listing not available in SDK")
            return self.admin.list_users(params or {})

        def create_user(self, email: str, password: str, user_metadata: dict[str, Any] | None = None, email_confirm: bool = False) -> Any:
            if not self.admin:
                raise NotImplementedError("Admin user creation not available in SDK")
            return self.admin.create_user(
                email=email,
                password=password,
                user_metadata=user_metadata,
                email_confirm=email_confirm,
            )

        def delete_user(self, user_id: str, should_soft_delete: bool = False) -> Any:
            if not self.admin:
                raise NotImplementedError("Admin user deletion not available in SDK")
            return self.admin.delete_user(user_id, should_soft_delete=should_soft_delete)

        def invite_user_by_email(self, email: str, options: dict[str, Any] | None = None) -> Any:
            if not self.admin:
                raise NotImplementedError("Admin invite not available in SDK")
            return self.admin.invite_user_by_email(email, options or {})

        def generate_link(self, params: dict[str, Any]) -> Any:
            if not self.admin:
                raise NotImplementedError("Admin generate_link not available in SDK")
            return self.admin.generate_link(params)

        def update_user_by_id(self, user_id: str, attributes: dict[str, Any]) -> Any:
            if not self.admin:
                raise NotImplementedError("Admin user update not available in SDK")
            return self.admin.update_user_by_id(user_id, attributes)

        def delete_mfa_factor(self, factor_id: str, user_id: str) -> Any:
            if not self.admin or not hasattr(self.admin, "mfa"):
                raise NotImplementedError("Admin MFA management not available in SDK")
            return self.admin.mfa.delete_factor({"id": factor_id, "user_id": user_id})

    class MFA:
        def __init__(self, auth):
            self.mfa = getattr(auth, "mfa", None)

        def enroll(self, factor_type: str = "totp", friendly_name: str = "") -> Any:
            if not self.mfa:
                raise NotImplementedError("MFA is not available in this SDK version")
            return self.mfa.enroll({"factor_type": factor_type, "friendly_name": friendly_name})

        def challenge(self, factor_id: str) -> Any:
            if not self.mfa:
                raise NotImplementedError("MFA is not available in this SDK version")
            return self.mfa.challenge({"factor_id": factor_id})

        def verify(self, factor_id: str, challenge_id: str, code: str) -> Any:
            if not self.mfa:
                raise NotImplementedError("MFA is not available in this SDK version")
            return self.mfa.verify({"factor_id": factor_id, "challenge_id": challenge_id, "code": code})

        def challenge_and_verify(self, factor_id: str, code: str) -> Any:
            if not self.mfa:
                raise NotImplementedError("MFA is not available in this SDK version")
            return self.mfa.challenge_and_verify({"factor_id": factor_id, "code": code})

        def unenroll(self, factor_id: str) -> Any:
            if not self.mfa:
                raise NotImplementedError("MFA is not available in this SDK version")
            return self.mfa.unenroll({"factor_id": factor_id})

        def get_authenticator_assurance_level(self) -> Any:
            if not self.mfa:
                raise NotImplementedError("MFA is not available in this SDK version")
            return self.mfa.get_authenticator_assurance_level()

    class Session:
        def __init__(self, auth):
            self.auth = auth

        def get_session(self) -> Any:
            return self.auth.get_session()

        def refresh_access_token(self, refresh_token: str) -> Any:
            return self.auth.refresh_session(refresh_token)

        def sign_out(self) -> Any:
            return self.auth.sign_out()

        def set_session(self, data: dict[str, Any]) -> Any:
            return self.auth.set_session(data)

    class User:
        def __init__(self, auth):
            self.auth = auth

        def create(self, email: str, password: str, user_metadata: dict[str, Any] | None = None) -> Any:
            return self.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": user_metadata} if user_metadata else None,
            })

        def create_anonymous(self) -> Any:
            return self.auth.sign_in_anonymously()

        def sign_in_with_email(self, email: str, password: str) -> Any:
            return self.auth.sign_in_with_password({"email": email, "password": password})

        def sign_in_with_id_token(self, provider: str, id_token: str) -> Any:
            return self.auth.sign_in_with_id_token({"provider": provider, "id_token": id_token})

        def sign_in_with_otp(self, email: str) -> Any:
            return self.auth.sign_in_with_otp({"email": email})

        def verify_otp(self, email: str, token: str, type: str = "email") -> Any:
            return self.auth.verify_otp({"email": email, "token": token, "type": type})

        def sign_in_with_oauth(self, provider: str, redirect_url: str) -> Any:
            return self.auth.sign_in_with_oauth({"provider": provider, "redirect_to": redirect_url})

        def sign_in_with_sso(self, domain: str = None, provider_id: str = None) -> Any:
            if domain:
                return self.auth.sign_in_with_sso(domain=domain)
            elif provider_id:
                return self.auth.sign_in_with_sso(provider_id=provider_id)
            else:
                raise ValueError(
                    "Either domain or provider_id must be provided for SSO sign-in."
                )

        def link_identity(self, provider: str, redirect_url: str) -> Any:
            return self.auth.link_identity({"provider": provider, "redirect_to": redirect_url})

        def unlink_identity(self, identity_id: str) -> Any:
            return self.auth.unlink_identity(identity_id)

        def get_user(self) -> Any:
            return self.auth.get_user()

        def update_user(self, user_data: dict[str, Any]) -> Any:
            return self.auth.update_user(user_data)

        def get_user_by_token(self, token: str) -> Any:
            return self.auth.get_user(token)

        def get_user_identities(self, user_id: str) -> Any:
            return self.auth.get_user_identities(user_id)

        def reset_password(self, email: str) -> Any:
            return self.auth.reset_password_email(email)
