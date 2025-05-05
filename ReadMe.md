# Supabase Python Integration Template

This template provides a production-ready integration for Supabase with Python applications using the official Supabase Python SDK. It includes modular, testable service classes for all major Supabase features, with best-practices for security, type safety, and maintainability.

## Features

- **Unified Supabase SDK integration** (async, service-role aware)
- **Modular Service Classes**:
  - `SupabaseAuthService` (with nested `admin`, `mfa_service`, `user`, and `session` domains)
  - `SupabaseStorageService` (with nested `bucket` and `file` domains)
  - Edge Functions, Realtime, and Database support
- **Admin & MFA Support**: Full admin user management and multi-factor authentication using the latest SDK idioms
- **RLS Bypass for Admin**: Secure use of service role key for privileged operations
- **Type-checked, documented, and linted** (PEP 604, Ruff, Pydantic v2 conventions)
- **Ready-to-use test suite** (pytest, FastAPI, async/await)
- **Django/FastAPI compatible**
- **Production best practices**: Secure secrets, DRY/SOLID, CI/CD, robust error handling, logging, and monitoring

## Requirements

- Python 3.8+
- [Supabase](https://supabase.com) project (obtain URL, anon key, and service role key)
- `supabase-py` (latest, async version)
- `httpx`, `pydantic`, `ruff`, `pytest`, etc.

## Installation

1. Clone this repository:

   ```bash
   git clone <your-repo-url>
   cd <your-repo>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables (see `.env.example`):

   ```env
   SUPABASE_URL=...           # Your Supabase project URL
   SUPABASE_ANON_KEY=...      # Your Supabase anon/public key
   SUPABASE_SERVICE_ROLE_KEY=... # Your Supabase service role key (admin ops)
   ```

## Usage

### Auth Service Example

```python
from app.core.third_party_integrations.supabase_home.sdk.auth import SupabaseAuthService
svc = SupabaseAuthService()

# User sign up
svc.user.create("user@email.com", "password123", user_metadata={"role": "basic"})

# Admin: list users
svc.admin.list_users()

# MFA: enroll TOTP
svc.mfa_service.enroll(factor_type="totp", friendly_name="My Auth App")
```

### Storage Service Example

```python
from app.core.third_party_integrations.supabase_home.sdk.storage import SupabaseStorageService
storage = SupabaseStorageService()

# Create a bucket
storage.bucket.create("my_bucket", {"public": True})

# Upload a file
with open("logo.png", "rb") as f:
    storage.file.upload("my_bucket", "logo.png", f, {"upsert": True})

# Get a signed URL
storage.file.create_signed_url("my_bucket", "logo.png", expires_in=3600)
```

### Using the Service Role Client

For admin operations (bypassing RLS), use the `SupabaseUnsecureService` which always uses the service role key:

```python
from app.core.third_party_integrations.supabase_home._service import SupabaseUnsecureService
svc = SupabaseUnsecureService()
# svc.raw is an AsyncClient with admin privileges
```

## Linting & Testing

- Run Ruff for linting:
  ```bash
  ruff check --fix .
  ```
- Run tests:
  ```bash
  pytest
  ```

## Best Practices
- Store secrets in environment variables, never in code
- Use service role key only on trusted backend/server code
- Follow DRY, SOLID, and CI/CD principles
- See `_docs/` for more patterns and usage

---

For more details, see the individual service files and code comments.
