import logging
import random
from collections.abc import Callable
from typing import Any

from fastapi import HTTPException

from app.core.third_party_integrations.supabase_home.client import get_supabase_client

logger = logging.getLogger(__name__)

class SupabaseRealtimeService:
    """
    Service for managing Supabase Realtime subscriptions using the official SDK patterns.
    Supports subscribing, broadcasting, and channel management.
    """

    def __init__(self, client):
        self.client = client
        self.active_channels = {}

async def get_realtime_service():
    client = await get_supabase_client()
    return SupabaseRealtimeService(client)

    def subscribe_to_channel(
        self,
        channel_name: str,
        event: str = None,
        on_broadcast: Callable = None,
        on_subscribe: Callable = None,
    ) -> Any:
        """
        Subscribe to a Realtime channel and optionally listen for broadcasts.
        Args:
            channel_name: Channel name (e.g., "room1")
            event: Broadcast event name to listen for (optional)
            on_broadcast: Callback for broadcast events (optional)
            on_subscribe: Callback for subscribe status (optional)
        Returns:
            The channel object
        """
        channel = self.client.channel(channel_name)
        if event and on_broadcast:
            channel.on_broadcast(event=event, callback=on_broadcast)
        if on_subscribe:
            channel.subscribe(on_subscribe)
        else:
            channel.subscribe()
        self.active_channels[channel_name] = channel
        return channel

    def send_broadcast(self, channel_name: str, event: str, payload: dict[str, Any]) -> None:
        """
        Broadcast a message to all connected clients to a channel.
        Args:
            channel_name: Channel name
            event: Broadcast event name
            payload: Data to broadcast
        """
        channel = self.active_channels.get(channel_name)
        if not channel:
            raise ValueError(f"Channel '{channel_name}' is not active.")
        channel.send_broadcast(event, payload)

    def remove_channel(self, channel_name: str) -> None:
        """
        Remove/unsubscribe from a channel and clean up.
        Args:
            channel_name: Channel name
        """
        channel = self.active_channels.pop(channel_name, None)
        if channel:
            self.client.remove_channel(channel)

    def remove_all_channels(self) -> None:
        """
        Remove/unsubscribe from all channels.
        """
        for channel in list(self.active_channels.values()):
            self.client.remove_channel(channel)
        self.active_channels.clear()

    def get_channels(self) -> list[Any]:
        """
        Retrieve all active channel objects.
        Returns:
            list of channel objects
        """
        return list(self.active_channels.values())

# Example usage:
# def handle_broadcast(payload):
#     print("Cursor position received!", payload)
# def on_subscribe(status, err):
#     if status == RealtimeSubscribeStates.SUBSCRIBED:
#         channel.send_broadcast("cursor-pos", {"x": random.random(), "y": random.random()})
# service = SupabaseRealtimeService()
# channel = service.subscribe_to_channel(
#     "room1",
#     event="cursor-pos",
#     on_broadcast=handle_broadcast,
#     on_subscribe=on_subscribe,
# )
