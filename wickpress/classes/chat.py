
from __future__ import annotations

import json
import hashlib
import reflex as rx

class ChatFull(rx.Base):
    chat_id: str
    chat_details: dict
    owner: str
    owner_handle: str
    created_at: str
    permissions: dict[str, bool]
    participant_ids: list[str] | None
    moderator_ids: list[str] | None
    messages: list[dict[str, str | dict]]
    hash: str | None

    is_group_chat: bool

    @classmethod
    def from_dict(cls, dict: dict) -> ChatFull:
        """
        Returns instance of ChatFull using a dict of values.
        """
        return cls(
            chat_id = dict["chat_id"],
            chat_details = dict["chat_details"],
            owner=dict["owner"],
            owner_handle=dict["owner_handle"],
            created_at=dict["created_at"],
            permissions=dict["permissions"],
            participant_ids=dict["participant_ids"],
            moderator_ids=dict["moderator_ids"],
            messages=dict["messages"],
            hash=dict["hash"],
            is_group_chat=True if len(dict["participant_ids"]) > 1 else False
        )
    
    def to_dict(self) -> dict:
        """
        Writes instance data to a dict for database ops.
        """
        return {
            "chat_id": self.chat_id,
            "chat_details": {
                "name": self.chat_details["name"],
                "description": self.chat_details["description"]
            },
            "owner": self.owner,
            "owner_handle": self.owner_handle,
            "created_at": self.created_at,
            "permissions": {
                "allow_chat": self.permissions["allow_chat"],
                "allow_interactions": self.permissions["allow_interactions"],
                "allow_invites": self.permissions["allow_invites"]
            },
            "participant_ids": self.participant_ids,
            "moderator_ids": self.moderator_ids,
            "messages": self.messages,
            "hash": self.hash
        }
    
    def hash_self(self) -> None:
        """
        Updates own hash value using instance data.
        """
        attr_dict = {
            "chat_id": self.chat_id,
            "chat_details": self.chat_details,
            "owner": self.owner,
            "owner_handle": self.owner_handle,
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
        self.hash = hasher.hexdigest()

    def to_hash(self) -> str:
        """
        Calc a sha256 from the columns stored in class.
        """
        attr_dict = {
            "chat_id": self.chat_id,
            "chat_details": self.chat_details,
            "owner": self.owner,
            "owner_handle": self.owner_handle,
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

    is_group_chat: bool
