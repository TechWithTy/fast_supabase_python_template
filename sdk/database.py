from typing import Any

from app.core.third_party_integrations.supabase_home._client import get_supabase_client


class SupabaseDatabaseService:
    """
    Service for interacting with Supabase Database (PostgreSQL) using supabase-py SDK.
    Provides methods for table, row, and function operations.
    """

    def __init__(self):
        self.client = get_supabase_client()

    def fetch_data(
        self,
        table: str,
        select: str = "*",
        filters: dict[str, Any] | None = None,
        order: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch data from a table with optional filtering, ordering, and pagination.
        """
        query = self.client.table(table).select(select)
        if filters:
            for k, v in filters.items():
                query = query.eq(k, v)
        if order:
            query = query.order(order)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = (
                query.range(offset, offset + (limit or 0) - 1)
                if limit
                else query.range(offset, 999999)
            )
        return query.execute().data

    def insert_data(
        self,
        table: str,
        data: dict[str, Any] | list[dict[str, Any]],
        upsert: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Insert data into a table.
        """
        query = self.client.table(table)
        if upsert:
            return query.upsert(data).execute().data
        return query.insert(data).execute().data

    def update_data(
        self,
        table: str,
        data: dict[str, Any],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Update data in a table.
        """
        query = self.client.table(table)
        for k, v in filters.items():
            query = query.eq(k, v)
        return query.update(data).execute().data

    def upsert_data(
        self,
        table: str,
        data: dict[str, Any] | list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Upsert data in a table (insert or update).
        """
        return self.insert_data(table, data, upsert=True)

    def delete_data(self, table: str, filters: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Delete data from a table.
        """
        query = self.client.table(table)
        for k, v in filters.items():
            query = query.eq(k, v)
        return query.delete().execute().data

    def call_function(
        self,
        function_name: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Call a PostgreSQL function (RPC).
        """
        return self.client.rpc(function_name, params or {}).execute().data

    def create_test_table(self, table: str) -> Any:
        """
        Create a simple test table for integration tests (via SQL RPC).
        """
        sql = f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            user_id TEXT
        );
        -- Set up RLS policies
        ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;
        -- Create policy to allow all operations for authenticated users
        DROP POLICY IF EXISTS \"Allow all operations for authenticated users\" ON {table};
        CREATE POLICY \"Allow all operations for authenticated users\"
        ON {table}
        FOR ALL
        TO authenticated
        USING (true)
        WITH CHECK (true);
        """
        return self.client.rpc("exec_sql", {"query": sql}).execute().data

    def delete_table(self, table: str) -> Any:
        """
        Delete a table from the database (via SQL RPC).
        """
        sql = f"DROP TABLE IF EXISTS {table};"
        return self.client.rpc("exec_sql", {"query": sql}).execute().data


# ! All logic now uses the official SDK, removing manual HTTP calls and custom base service logic.
# ? Some advanced or admin features may not be available in all SDK versions.
# * Add/adjust type hints for SDK return values as your supabase-py version allows.
# todo: Test all flows and adapt as SDK evolves.
