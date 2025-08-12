
import reflex as rx

from datetime import datetime

class ChatFull(rx.Base):
    chat_id: str
    chat_details: dict
    owner: str
    created_at: datetime
    participant_ids: list
    moderator_ids: list
    permissions: dict
    messages: list

class ChatLimited(rx.Base):
    chat_id: str
    chat_details: dict
    owner: str
    participant_ids: list[str]
