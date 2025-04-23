from enum import Enum

class EventType(str, Enum):
    PLAYER_JOINED = "player_joined"
    PLAYER_READY = "player_ready"
    GAME_START = "game_start"
    TURN_STARTED = "turn_started"
    CARD_ACTION = "card_action"
    CARD_MOVED = "card_moved"
    UPDATE_LORE = "update_lore"
    GAME_END = "game_end"
    CHAT_MESSAGE = "chat_message"
    PLAYER_DISCONNECTED = "player_disconnected"
    PLAYER_RECONNECTED = "player_reconnected"
    ERROR = "error"

def make_event(event_type: EventType, payload: dict) -> dict:
    return {
        "type": event_type.value,
        "payload": payload
    }
