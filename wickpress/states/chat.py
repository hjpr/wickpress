
import reflex as rx
import hashlib
import time

from datetime import datetime, timezone
from rich.console import Console
from typing import Callable, Iterable

from ..classes.chat import ChatLimited
from .user import UserState

console = Console()

CHAT_REFRESH_RATE = 5 # (Interval after which another refresh is allowed - seconds)
CHAT_SEND_LIMIT_RATE = 5 # (Interval after which user can send another message - seconds)

class ChatState(UserState):

    loading_chats: bool
    loading_participants: bool
    new_chat_modal_open: bool

    selected_filter: str = "All"

    participant: str
    no_participants: str
    participants_available: list[dict[str, str]]
    participants_selected: list[dict[str, str]]
    content: str

    chats: list[ChatLimited]

    @rx.var
    def participant_popup_open(self) -> bool:
        return True if self.participant else False

    def set_participant(self, participant:str) -> Iterable[Callable]:
        """
        Set participant if user entered, otherwise reset back to default.
        """
        self.participant = participant
        if len(participant) > 0:
            self.query_participant(participant)
        else:
            self.participants = ""
            self.no_participants = ""
            self.loading_participants = False

    def query_participant(self, participant: str) -> None:
        """
        Perform a partial match search for user entered participant.
        """
        try:
            valid_participants = (
                self.query()
                .admin()
                .table("profiles")
                .select("*")
                .ilike("handle", f"{participant}%")
                .limit(10)
                .execute()
            )
            self.participants_available = valid_participants
            # Prevents UI delay from showing a valid search as invalid for a brief second
            if not valid_participants:
                self.no_participants = self.participants
        except:
            console.print_exception()
        finally:
            self.loading_participants = False

    def load_chats(self) -> None:
        """
        Pull chats down where user is participant.
        Load chats as ChatLimited classes.
        """
        try:
            participant_chats = (
                self.query()
                .table("chats")
                .select("chat_id,chat_details,owner,participant_ids")
                .contains("participant_ids", [self.user["wickpress"]["id"]])
                .execute()
            )
            all_chats = []
            for chat in participant_chats:
                chat_object = ChatLimited(
                    chat_id=chat["chat_id"],
                    chat_details=chat["chat_details"],
                    owner=chat["owner"],
                    participant_ids=chat["participant_ids"]
                )
                all_chats.append(chat_object)
            self.chats = all_chats

        except Exception as e: 
            console.print_exception()
        finally:
            self.loading_chats = False

class ViewChatState(ChatState):
    chat_id: str
    chat_details: str
    owner: str
    created_at: datetime
    permissions: dict[str, bool]
    participant_ids: list[str]
    moderator_ids: list[str]
    messages: list[dict[str, str]]
    chat_content: str
    last_submitted_message: int

    CHAT_TIMEOUT_INTERVAL_SEC = 5

    def load_messages(self) -> None:
        messages = (
            self.query()
            .table("chats")
            .select("*")
            .eq("chat_id", self.chat_id)
            .execute()
        )
        self.messages = messages

    def send_message(self) -> None:
        content = self.chat_content
        message = {
            "user_id": self.user["wickpress"]["id"],
            "content": content,
            "timestamp": str(datetime.now(timezone.utc).isoformat(timespec="seconds"))
        }
        current_time = time.time()
        if self.last_submitted_message:
            if current_time - self.last_submitted_message < 5:
                return
        updated_messages = self.messages.append(message)
        try:
            (
                self.query()
                .table("chats")
                .insert({"messages": updated_messages}, return_="minimal")
                .execute()
            )
            self.messages = updated_messages
        except Exception:
            console.print_exception()

