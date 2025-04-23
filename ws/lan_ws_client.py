import asyncio
import websockets
import json
from ws_events import EventType, make_event

class FineTableClient:
    def __init__(self, uri, player_id, name, deck):
        self.uri = uri
        self.player_id = player_id
        self.name = name
        self.deck = deck

    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket
            await self.send_event(EventType.PLAYER_JOINED, {
                "player_id": self.player_id,
                "name": self.name,
                "deck": self.deck
            })
            await self.listen()

    async def send_event(self, event_type, payload):
        event = make_event(event_type, payload)
        await self.websocket.send(json.dumps(event))

    async def listen(self):
        try:
            async for message in self.websocket:
                data = json.loads(message)
                print(f"[RECEIVED] {data['type']} -> {data['payload']}")
                if data['type'] == EventType.TURN_STARTED:
                    await self.manual_input_loop()
        except websockets.exceptions.ConnectionClosed:
            print("Disconnected from server.")

    async def manual_input_loop(self):
        while True:
            action = input("Enter action (quest/play/ink/lore/end): ").strip().lower()
            if action == "end":
                break
            elif action == "lore":
                await self.send_event(EventType.UPDATE_LORE, {
                    "player_id": self.player_id,
                    "amount": 1
                })
            else:
                card_id = input("Enter card ID: ").strip()
                await self.send_event(EventType.CARD_ACTION, {
                    "player_id": self.player_id,
                    "card_id": card_id,
                    "action": action,
                    "target": "none",
                    "zone": "play"
                })

if __name__ == "__main__":
    player_deck = {
        "name": "Steel Amethyst Tempo",
        "cards": ["card_id_001", "card_id_002", "card_id_003"]
    }
    client = FineTableClient("ws://localhost:8765", "p2", "Greg", player_deck)
    asyncio.run(client.connect())
