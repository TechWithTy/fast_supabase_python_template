from typing import Any, BinaryIO

from app.core.third_party_integrations.supabase_home._client import get_supabase_client


class SupabaseStorageService:
    """
    Service for interacting with Supabase Storage API using the official SDK patterns.
    Provides methods for bucket and file operations, matching the supabase-py API.
    Grouped into logical nested classes: Bucket and File.
    """
    def __init__(self):
        self.client = get_supabase_client()
        self.storage = self.client.storage
        self.bucket = self.Bucket(self.storage)
        self.file = self.File(self.storage)

    class Bucket:
        def __init__(self, storage):
            self.storage = storage

        def create(self, bucket_id: str, options: dict[str, Any]) -> Any:
            return self.storage.create_bucket(bucket_id, options=options)

        def get(self, bucket_id: str) -> Any:
            return self.storage.get_bucket(bucket_id)

        def list(self) -> Any:
            return self.storage.list_buckets()

        def update(self, bucket_id: str, options: dict[str, Any]) -> Any:
            return self.storage.update_bucket(bucket_id, options=options)

        def delete(self, bucket_id: str) -> Any:
            return self.storage.delete_bucket(bucket_id)

        def empty(self, bucket_id: str) -> Any:
            return self.storage.empty_bucket(bucket_id)

    class File:
        def __init__(self, storage):
            self.storage = storage

        def upload(self, bucket_id: str, path: str, file: BinaryIO | bytes | str, file_options: dict[str, Any]) -> Any:
            return self.storage.from_(bucket_id).upload(file=file, path=path, file_options=file_options)

        def download(self, bucket_id: str, path: str) -> bytes:
            return self.storage.from_(bucket_id).download(path)

        def list(self, bucket_id: str, folder: str = "", options: dict[str, Any] | None = None) -> Any:
            return self.storage.from_(bucket_id).list(folder, options or {})

        def update(self, bucket_id: str, path: str, file: BinaryIO | bytes | str, file_options: dict[str, Any]) -> Any:
            return self.storage.from_(bucket_id).update(file=file, path=path, file_options=file_options)

        def move(self, bucket_id: str, from_path: str, to_path: str) -> Any:
            return self.storage.from_(bucket_id).move(from_path, to_path)

        def copy(self, bucket_id: str, from_path: str, to_path: str) -> Any:
            return self.storage.from_(bucket_id).copy(from_path, to_path)

        def remove(self, bucket_id: str, paths: list[str]) -> Any:
            return self.storage.from_(bucket_id).remove(paths)

        def create_signed_url(self, bucket_id: str, path: str, expires_in: int, options: dict[str, Any] | None = None) -> Any:
            return self.storage.from_(bucket_id).create_signed_url(path, expires_in, options or {})

        def create_signed_urls(self, bucket_id: str, paths: list[str], expires_in: int, options: dict[str, Any] | None = None) -> Any:
            return self.storage.from_(bucket_id).create_signed_urls(paths, expires_in, options or {})

        def create_signed_upload_url(self, bucket_id: str, path: str) -> Any:
            return self.storage.from_(bucket_id).create_signed_upload_url(path)

        def upload_to_signed_url(self, bucket_id: str, path: str, token: str, file: BinaryIO | bytes | str, file_options: dict[str, Any]) -> Any:
            return self.storage.from_(bucket_id).upload_to_signed_url(path, token, file=file, file_options=file_options)

        def get_public_url(self, bucket_id: str, path: str, options: dict[str, Any] | None = None) -> Any:
            return self.storage.from_(bucket_id).get_public_url(path, options or {})
