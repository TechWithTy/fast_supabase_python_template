from typing import Any, BinaryIO
from app.core.third_party_integrations.supabase_home._client import get_supabase_client

class SupabaseStorageService:
    """
    Service for interacting with Supabase Storage API using the official SDK patterns.
    Provides methods for bucket and file operations, matching the supabase-py API.
    """
    def __init__(self):
        self.client = get_supabase_client()
        self.storage = self.client.storage

    def create_bucket(self, bucket_id: str, options: dict[str, Any]) -> Any:
        """
        Creates a new storage bucket.
        Args:
            bucket_id: Unique identifier for the bucket
            options: Dict of options (public, allowed_mime_types, file_size_limit, etc)
        Returns:
            Response from SDK
        """
        return self.storage.create_bucket(bucket_id, options=options)

    def get_bucket(self, bucket_id: str) -> Any:
        """
        Retrieves details of an existing bucket.
        Args:
            bucket_id: Unique identifier for the bucket
        Returns:
            Bucket details
        """
        return self.storage.get_bucket(bucket_id)

    def list_buckets(self) -> Any:
        """
        Retrieves details of all buckets in the project.
        Returns:
            List of buckets
        """
        return self.storage.list_buckets()

    def update_bucket(self, bucket_id: str, options: dict[str, Any]) -> Any:
        """
        Updates a storage bucket.
        Args:
            bucket_id: Unique identifier for the bucket
            options: Dict of options to update
        Returns:
            Updated bucket details
        """
        return self.storage.update_bucket(bucket_id, options=options)

    def delete_bucket(self, bucket_id: str) -> Any:
        """
        Deletes an existing bucket. Bucket must be empty.
        Args:
            bucket_id: Unique identifier for the bucket
        Returns:
            Deletion response
        """
        return self.storage.delete_bucket(bucket_id)

    def empty_bucket(self, bucket_id: str) -> Any:
        """
        Removes all objects inside a bucket.
        Args:
            bucket_id: Unique identifier for the bucket
        Returns:
            Response from SDK
        """
        return self.storage.empty_bucket(bucket_id)

    def upload_file(self, bucket_id: str, path: str, file: BinaryIO | bytes | str, file_options: dict[str, Any]) -> Any:
        """
        Uploads a file to an existing bucket.
        Args:
            bucket_id: Bucket name
            path: File path (e.g., 'folder/file.png')
            file: File data (open file, bytes, or string)
            file_options: Dict of file options (e.g., cache-control, upsert)
        Returns:
            Upload response
        """
        return self.storage.from_(bucket_id).upload(
            file=file, path=path, file_options=file_options
        )

    def download_file(self, bucket_id: str, path: str) -> bytes:
        """
        Downloads a file from a bucket.
        Args:
            bucket_id: Bucket name
            path: File path
        Returns:
            File bytes
        """
        return self.storage.from_(bucket_id).download(path)

    def list_files(self, bucket_id: str, folder: str = "", options: dict[str, Any] | None = None) -> Any:
        """
        Lists all files in a bucket or folder.
        Args:
            bucket_id: Bucket name
            folder: Folder path (optional)
            options: Dict of search options (optional)
        Returns:
            List of files
        """
        return self.storage.from_(bucket_id).list(folder, options or {})

    def update_file(self, bucket_id: str, path: str, file: BinaryIO | bytes | str, file_options: dict[str, Any]) -> Any:
        """
        Replaces an existing file at the specified path.
        Args:
            bucket_id: Bucket name
            path: File path
            file: File data
            file_options: Dict of file options (e.g., cache-control, upsert)
        Returns:
            Update response
        """
        return self.storage.from_(bucket_id).update(
            file=file, path=path, file_options=file_options
        )

    def move_file(self, bucket_id: str, from_path: str, to_path: str) -> Any:
        """
        Moves an existing file to a new path in the same bucket.
        Args:
            bucket_id: Bucket name
            from_path: Original file path
            to_path: New file path
        Returns:
            Move response
        """
        return self.storage.from_(bucket_id).move(from_path, to_path)

    def copy_file(self, bucket_id: str, from_path: str, to_path: str) -> Any:
        """
        Copies an existing file to a new path in the same bucket.
        Args:
            bucket_id: Bucket name
            from_path: Original file path
            to_path: New file path
        Returns:
            Copy response
        """
        return self.storage.from_(bucket_id).copy(from_path, to_path)

    def remove_files(self, bucket_id: str, paths: list[str]) -> Any:
        """
        Deletes files within the same bucket.
        Args:
            bucket_id: Bucket name
            paths: List of file paths to delete
        Returns:
            Remove response
        """
        return self.storage.from_(bucket_id).remove(paths)

    def create_signed_url(self, bucket_id: str, path: str, expires_in: int, options: dict[str, Any] | None = None) -> Any:
        """
        Creates a signed URL for a file.
        Args:
            bucket_id: Bucket name
            path: File path
            expires_in: Expiry in seconds
            options: Dict of URL options (optional)
        Returns:
            Signed URL response
        """
        return self.storage.from_(bucket_id).create_signed_url(path, expires_in, options or {})

    def create_signed_urls(self, bucket_id: str, paths: list[str], expires_in: int, options: dict[str, Any] | None = None) -> Any:
        """
        Creates multiple signed URLs for files.
        Args:
            bucket_id: Bucket name
            paths: List of file paths
            expires_in: Expiry in seconds
            options: Dict of URL options (optional)
        Returns:
            Signed URLs response
        """
        return self.storage.from_(bucket_id).create_signed_urls(paths, expires_in, options or {})

    def create_signed_upload_url(self, bucket_id: str, path: str) -> Any:
        """
        Creates a signed upload URL for a file.
        Args:
            bucket_id: Bucket name
            path: File path
        Returns:
            Signed upload URL response
        """
        return self.storage.from_(bucket_id).create_signed_upload_url(path)

    def upload_to_signed_url(self, bucket_id: str, path: str, token: str, file: BinaryIO | bytes | str, file_options: dict[str, Any]) -> Any:
        """
        Uploads a file with a token generated from create_signed_upload_url.
        Args:
            bucket_id: Bucket name
            path: File path
            token: Signed upload token
            file: File data
            file_options: Dict of file options
        Returns:
            Upload response
        """
        return self.storage.from_(bucket_id).upload_to_signed_url(
            path=path, token=token, file=file, file_options=file_options
        )

    def get_public_url(self, bucket_id: str, path: str, options: dict[str, Any] | None = None) -> Any:
        """
        Retrieves the public URL for an asset in a public bucket.
        Args:
            bucket_id: Bucket name
            path: File path
            options: Dict of URL options (optional)
        Returns:
            Public URL response
        """
        return self.storage.from_(bucket_id).get_public_url(path, options or {})
