import asyncio
import websockets
import json
from ws_events import EventType, make_event

CONNECTED_CLIENTS = set()
PLAYER_REGISTRY = {}
TURN_ORDER = []

def broadcast(event):
    message = json.dumps(event)
    return [client.send(message) for client in CONNECTED_CLIENTS]

async def handle_client(websocket):
    CONNECTED_CLIENTS.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            event_type = data.get("type")
            payload = data.get("payload")

            if event_type == EventType.PLAYER_JOINED:
                player_id = payload["player_id"]
                PLAYER_REGISTRY[player_id] = websocket
                TURN_ORDER.append(player_id)
                await asyncio.gather(*broadcast(make_event(EventType.PLAYER_JOINED, payload)))

            elif event_type == EventType.PLAYER_READY:
                await asyncio.gather(*broadcast(make_event(EventType.PLAYER_READY, payload)))

            elif event_type == EventType.GAME_START:
                await asyncio.gather(*broadcast(make_event(EventType.GAME_START, payload)))

            elif event_type == EventType.TURN_STARTED:
                await asyncio.gather(*broadcast(make_event(EventType.TURN_STARTED, payload)))

            elif event_type == EventType.CARD_ACTION:
                await asyncio.gather(*broadcast(make_event(EventType.CARD_ACTION, payload)))

            elif event_type == EventType.CARD_MOVED:
                await asyncio.gather(*broadcast(make_event(EventType.CARD_MOVED, payload)))

            elif event_type == EventType.UPDATE_LORE:
                await asyncio.gather(*broadcast(make_event(EventType.UPDATE_LORE, payload)))

            elif event_type == EventType.GAME_END:
                await asyncio.gather(*broadcast(make_event(Event_*
