from typing import Any

from .._client import get_supabase_client  # ! Use the unified client

class SupabaseAuthService:
    """
    Service for interacting with Supabase Auth API using official supabase-py SDK.
    Provides methods for user management, authentication, session handling, MFA, and admin operations.
    """

    def __init__(self):
        self.client = get_supabase_client()
        self.auth = self.client.auth
        self.admin_auth = getattr(self.auth, "admin", None)  # For admin ops if SDK supports
        self.mfa = getattr(self.auth, "mfa", None)  # For MFA if SDK supports

    # --- MFA Methods ---
    def enroll_mfa_factor(self, factor_type: str = "totp", friendly_name: str = "") -> Any:
        """
        Enroll a new MFA factor (currently only 'totp' supported).
        Returns: MFA enrollment response
        """
        if not self.mfa:
            raise NotImplementedError("MFA is not available in this SDK version")
        return self.mfa.enroll({"factor_type": factor_type, "friendly_name": friendly_name})

    def challenge_mfa(self, factor_id: str) -> Any:
        """
        Create a challenge for an enrolled MFA factor.
        Returns: Challenge response
        """
        if not self.mfa:
            raise NotImplementedError("MFA is not available in this SDK version")
        return self.mfa.challenge({"factor_id": factor_id})

    def verify_mfa_challenge(self, factor_id: str, challenge_id: str, code: str) -> Any:
        """
        Verify a challenge for MFA.
        Returns: Verification response
        """
        if not self.mfa:
            raise NotImplementedError("MFA is not available in this SDK version")
        return self.mfa.verify({"factor_id": factor_id, "challenge_id": challenge_id, "code": code})

    def challenge_and_verify_mfa(self, factor_id: str, code: str) -> Any:
        """
        Create and verify a challenge in a single step.
        Returns: Challenge and verification response
        """
        if not self.mfa:
            raise NotImplementedError("MFA is not available in this SDK version")
        return self.mfa.challenge_and_verify({"factor_id": factor_id, "code": code})

    def unenroll_mfa_factor(self, factor_id: str) -> Any:
        """
        Unenroll an MFA factor.
        Returns: Unenroll response
        """
        if not self.mfa:
            raise NotImplementedError("MFA is not available in this SDK version")
        return self.mfa.unenroll({"factor_id": factor_id})

    def get_authenticator_assurance_level(self) -> Any:
        """
        Get the Authenticator Assurance Level (AAL) for the current user.
        Returns: AAL response
        """
        if not self.mfa:
            raise NotImplementedError("MFA is not available in this SDK version")
        return self.mfa.get_authenticator_assurance_level()

    # --- Admin Methods ---
    def get_user_by_id(self, user_id: str) -> Any:
        """
        Retrieve a user by their unique ID (admin only).
        """
        if not self.admin_auth:
            raise NotImplementedError("Admin user retrieval not available in SDK")
        return self.admin_auth.get_user_by_id(user_id)

    def list_users(self, params: dict[str, Any] | None = None) -> Any:
        """
        List all users (admin only).
        """
        if not self.admin_auth:
            raise NotImplementedError("Admin user listing not available in SDK")
        return self.admin_auth.list_users(params or {})

    def create_admin_user(self, email: str, password: str, user_metadata: dict[str, Any] | None = None, email_confirm: bool = False) -> Any:
        """
        Create a new user with admin privileges (if supported by SDK).
        """
        if not self.admin_auth:
            raise NotImplementedError("Admin user creation not available in SDK")
        return self.admin_auth.create_user(
            email=email,
            password=password,
            user_metadata=user_metadata,
            email_confirm=email_confirm,
        )

    def delete_user(self, user_id: str, should_soft_delete: bool = False) -> Any:
        """
        Delete a user by ID (admin only).
        """
        if not self.admin_auth:
            raise NotImplementedError("Admin user deletion not available in SDK")
        return self.admin_auth.delete_user(user_id, should_soft_delete=should_soft_delete)

    def invite_user_by_email(self, email: str, options: dict[str, Any] | None = None) -> Any:
        """
        Send an email invite link to a user (admin only).
        """
        if not self.admin_auth:
            raise NotImplementedError("Admin invite not available in SDK")
        return self.admin_auth.invite_user_by_email(email, options or {})

    def generate_link(self, params: dict[str, Any]) -> Any:
        """
        Generate an email link for signup, magiclink, invite, recovery, etc. (admin only).
        """
        if not self.admin_auth:
            raise NotImplementedError("Admin generate_link not available in SDK")
        return self.admin_auth.generate_link(params)

    def update_user_by_id(self, user_id: str, attributes: dict[str, Any]) -> Any:
        """
        Update a user's attributes by ID (admin only).
        """
        if not self.admin_auth:
            raise NotImplementedError("Admin user update not available in SDK")
        return self.admin_auth.update_user_by_id(user_id, attributes)

    def delete_mfa_factor_admin(self, factor_id: str, user_id: str) -> Any:
        """
        Delete a factor for a user (admin only).
        """
        if not self.admin_auth or not hasattr(self.admin_auth, "mfa"):
            raise NotImplementedError("Admin MFA management not available in SDK")
        return self.admin_auth.mfa.delete_factor({"id": factor_id, "user_id": user_id})

    # --- User/Session Methods ---
    def create_user(
        self, email: str, password: str, user_metadata: dict[str, Any] | None = None
    ) -> Any:
        """
        Create a new user with email and password using the SDK.
        """
        return self.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {"data": user_metadata} if user_metadata else None,
            }
        )

    def create_anonymous_user(self) -> Any:
        """
        Create an anonymous user using Supabase SDK.
        """
        return self.auth.sign_in_anonymously()

    def sign_in_with_email(self, email: str, password: str) -> Any:
        """
        Sign in a user with email and password using the SDK.
        """
        return self.auth.sign_in_with_password({"email": email, "password": password})

    def sign_in_with_id_token(self, provider: str, id_token: str) -> Any:
        """
        Sign in a user with an ID token from a third-party provider.
        """
        return self.auth.sign_in_with_id_token(
            {"provider": provider, "id_token": id_token}
        )

    def sign_in_with_otp(self, email: str) -> Any:
        """
        Send a one-time password to the user's email.
        """
        return self.auth.sign_in_with_otp({"email": email})

    def verify_otp(self, email: str, token: str, type: str = "email") -> Any:
        """
        Verify a one-time password and log in the user.
        """
        return self.auth.verify_otp({"email": email, "token": token, "type": type})

    def sign_in_with_oauth(self, provider: str, redirect_url: str) -> Any:
        """
        Get the URL to redirect the user for OAuth sign-in.
        """
        return self.auth.sign_in_with_oauth(
            {"provider": provider, "redirect_to": redirect_url}
        )

    def sign_in_with_sso(self, domain: str = None, provider_id: str = None) -> Any:
        """
        Sign in a user through SSO with a domain or provider_id using Supabase SDK.
        Args:
            domain: Organization domain for SSO (optional)
            provider_id: SSO provider ID (optional)
        Returns:
            SDK response object
        Raises:
            ValueError if neither domain nor provider_id is provided
        """
        if domain:
            return self.auth.sign_in_with_sso(domain=domain)
        elif provider_id:
            return self.auth.sign_in_with_sso(provider_id=provider_id)
        else:
            raise ValueError(
                "Either domain or provider_id must be provided for SSO sign-in."
            )

    def sign_out(self) -> Any:
        """
        Sign out the current user using the SDK.
        """
        return self.auth.sign_out()

    def reset_password(self, email: str) -> Any:
        """
        Send a password reset email using the SDK.
        """
        return self.auth.reset_password_email(email)

    def get_session(self) -> Any:
        """
        Retrieve the user's session (if supported by SDK).
        """
        return self.auth.get_session()

    def refresh_access_token(self, refresh_token: str) -> Any:
        """
        Refresh the user's access token using a refresh token (if supported by SDK).
        """
        # ! This is a wrapper for SDK's refresh_session for clarity
        return self.auth.refresh_session(refresh_token)

    def get_user(self) -> Any:
        """
        Get the currently authenticated user using the SDK.
        """
        return self.auth.get_user()

    def update_user(self, user_data: dict[str, Any]) -> Any:
        """
        Update a user's data (current user).
        """
        return self.auth.update_user(user_data)

    def get_user_by_token(self, token: str) -> Any:
        """
        Get user information from a JWT token (if supported by SDK).
        """
        return self.auth.get_user(token)

    def get_user_identities(self, user_id: str) -> Any:
        """
        Retrieve identities linked to a user (admin only, if supported).
        """
        return self.auth.get_user_identities(user_id)

    def link_identity(self, provider: str, redirect_url: str) -> Any:
        """
        Link an identity to a user (if supported by SDK).
        """
        return self.auth.link_identity({"provider": provider, "redirect_to": redirect_url})

    def unlink_identity(self, identity_id: str) -> Any:
        """
        Unlink an identity from a user (if supported by SDK).
        """
        return self.auth.unlink_identity(identity_id)

    def set_session_data(self, data: dict[str, Any]) -> Any:
        """
        Set session data (if supported by SDK).
        """
        return self.auth.set_session(data)
