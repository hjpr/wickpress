
import json
import hashlib
import reflex as rx

from datetime import datetime


class ChatFull(rx.Base):
    chat_id: str
    chat_details: dict
    owner: str
    created_at: str
    permissions: dict[str, bool]
    participant_ids: list[str] | None
    moderator_ids: list[str] | None
    messages: list[dict[str, str]]
    hash: str | None

    def num_messages(self) -> int:
        return len(self.messages)

    def to_hash(self) -> str:
        """
        Calc a sha256 from the columns stored in class.
        """
        attr_dict = {
            "chat_id": self.chat_id,
            "chat_details": self.chat_details,
            "owner": self.owner,
            "created_at": self.created_at,
            "permissions": self.permissions,
            "participant_ids": self.participant_ids,
            "moderator_ids": self.moderator_ids,
            "messages": self.messages
        }
        serialized_data = json.dumps(
            attr_dict,
            sort_keys=True
        ).encode("utf-8")

        hasher = hashlib.sha256()
        hasher.update(serialized_data)

        return hasher.hexdigest()


class ChatPartial(rx.Base):
    chat_id: str
    chat_details: dict
    owner: str
    owner_handle: str
    participant_ids: list[str]
    num_participants: int
    hash: str
