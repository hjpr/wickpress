
import reflex as rx
import hashlib
import json
import time

from datetime import datetime, timezone
from rich.console import Console
from typing import Any, Callable, Iterable

from ..classes.chat import ChatLimited
from ..states.page import PageState
from .user import UserState

console = Console()

CHAT_REFRESH_RATE = 5 # (Interval after which another refresh is allowed - seconds)
CHAT_SEND_LIMIT_RATE = 5 # (Interval after which user can send another message - seconds)

class ChatState(UserState):

    loading_all_chats: bool
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

    def load_all_chats(self) -> None:
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
            self.loading_all_chats = False

class ViewChatState(ChatState):
    # Helper vars
    CHAT_TIMEOUT_INTERVAL_SEC = 5
    loading_single_chat: bool

    # Cache to save previously viewed chats
    chat_cache: dict[str, dict[str, Any]]

    # Vars stored for a single chat.
    chat_id: str
    chat_details: dict
    owner: str
    created_at: str
    permissions: dict[str, bool]
    participant_ids: list[str] | None
    moderator_ids: list[str] | None
    messages: list[dict[str, str]] | None
    hash: str | None

    # Vars for submitting message to chat.
    chat_content: str
    last_submitted_message: int

    @staticmethod
    def create_hash(data_to_hash: dict) -> str:
        """
        Return a str of hexadecimal digits based on sha256 hasher.
        """
        serialized_data = json.dumps(
            data_to_hash,
            sort_keys=True
        ).encode("utf-8")

        hasher = hashlib.sha256()
        hasher.update(serialized_data)

        return hasher.hexdigest()

    def load_single_chat(self) -> Callable | None:
        self.loading_single_chat = True

        # If url param is empty, go back
        chat_id_from_url = self.router_data["query"]["chat_id_from_url"]
        if not chat_id_from_url:
            return rx.call_script(
                "history.back()",
                callback=PageState.default_script_callback
            )
        
        # Check if chat was previously loaded and up to date
        if chat_id_from_url in self.chat_cache:

            # Pull down hash from db and compare hash to cache
            cached_chat_hash = self.chat_cache[chat_id_from_url]["hash"]
            db_chat_hash = (
                self.query()
                .table("chats")
                .select("hash")
                .eq("chat_id", chat_id_from_url)
                .execute()[0]["hash"]
            )
            console.print(f"Comparing cached hash - {cached_chat_hash}")
            console.print(f"...to db hash - {db_chat_hash}")
            # Set cached chat to state instead of making db call if current with db
            if cached_chat_hash == db_chat_hash:
                chat: dict = self.chat_cache[chat_id_from_url]
                self.chat_id = chat["chat_id"]
                self.chat_details = chat["chat_details"]
                self.owner = chat["owner"]
                self.created_at = chat["created_at"]
                self.permissions = chat["permissions"]
                self.participant_ids = chat["participant_ids"]
                self.moderator_ids = chat["moderator_ids"]
                self.messages = chat["messages"]
                self.hash = chat["hash"]
                console.print(
                    f"Loaded {chat_id_from_url} from cache for {self.user["wickpress"]["handle"]}"
                )

                # Abort load from db
                return

        try:
            # Pull full object from database
            chat = (
                self.query()
                .table("chats")
                .select("*")
                .eq("chat_id", chat_id_from_url)
                .execute()
                [0]
            )

            # Load object into state
            self.chat_id = chat["chat_id"]
            self.chat_details = chat["chat_details"]
            self.owner = chat["owner"]
            self.created_at = chat["created_at"]
            self.permissions = chat["permissions"]
            self.participant_ids = chat["participant_ids"]
            self.moderator_ids = chat["moderator_ids"]
            self.messages = chat["messages"]

            # Save object under it's own chat_id
            self.chat_cache[chat["chat_id"]] = chat
            console.print(
                f"Loaded {chat_id_from_url} from database for {self.user["wickpress"]["handle"]}"
            )

        except Exception as e:
            console.print(str(e))
        finally:
            self.loading_single_chat = False

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

