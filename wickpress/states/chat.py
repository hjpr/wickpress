
import reflex as rx
import time
import uuid

from copy import deepcopy
from datetime import datetime, timezone
from reflex.event import EventSpec
from rich.console import Console
from typing import Generator

import wickpress

from ..classes.chat import ChatFull, ChatPartial
from ..states.page import PageState
from .user import UserState

console = Console()

CHAT_REFRESH_RATE = 5 # (Interval after which another refresh is allowed - seconds)
CHAT_SEND_LIMIT_RATE = 5 # (Interval after which user can send another message - seconds)
MAX_RETRIES = 3

class ChatState(UserState):

    loading_all_chats: bool
    loading_participants: bool
    participant_popup_open: bool

    selected_filter: str = "All"

    participant: str
    no_participants: str
    participants_available: list[dict[str, str]]
    participants_selected: list[dict[str, str]]

    chats: list[ChatPartial]

    def set_participant(self, participant: str) -> None:
        """
        Set participant if user entered, otherwise reset back to default.
        """
        self.participant = participant
        if len(participant) > 0:
            self.query_participant(participant)
            self.participant_popup_open = True
        else:
            self.no_participants = ""
            self.loading_participants = False
            self.participant_popup_open = False

    def set_participants_selected(self, participant: dict | list) -> None:
        if isinstance(participant, dict):
            if participant not in self.participants_selected:
                self.participants_selected.append(participant)
            self.participant = ""
            self.participant_popup_open = False
        else:
            self.participants_selected = participant

    def remove_participants(self, participant: str) -> None:
        if participant in self.participants_selected:
            self.participants_selected.remove(participant)

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
        except:
            console.print_exception()
        finally:
            self.loading_participants = False

    def load_all_chats(self) -> None:
        """
        Pull chats down where user is participant.
        Load chats as ChatPartial classes.
        """
        try:
            owner_chats = (
                self.query()
                .table("chats")
                .select("chat_id,chat_details,owner,owner_handle,participant_ids,hash")
                .eq("owner", self.user["wickpress"]["id"])
                .execute()
            )
            participant_chats = (
                self.query()
                .table("chats")
                .select("chat_id,chat_details,owner,owner_handle,participant_ids,hash")
                .contains("participant_ids", [self.user["wickpress"]["id"]])
                .execute()
            )
            all_chats = []
            for chat in owner_chats:
                chat_object = ChatPartial(
                    chat_id=chat["chat_id"],
                    chat_details=chat["chat_details"],
                    owner=chat["owner"],
                    owner_handle=chat["owner_handle"],
                    participant_ids=chat["participant_ids"],
                    num_participants=len(chat["participant_ids"]),
                    hash=chat["hash"],
                    is_group_chat=True if len(chat["participant_ids"]) > 1 else False
                )
                all_chats.append(chat_object)
            for chat in participant_chats:
                if chat["owner"] != self.user["wickpress"]["id"]:
                    chat_object = ChatPartial(
                        chat_id=chat["chat_id"],
                        chat_details=chat["chat_details"],
                        owner=chat["owner"],
                        owner_handle=chat["owner_handle"],
                        participant_ids=chat["participant_ids"],
                        num_participants=len(chat["participant_ids"]),
                        hash=chat["hash"],
                        is_group_chat=True if len(chat["participant_ids"]) > 1 else False
                    )
            self.chats = all_chats

        except Exception as e: 
            console.print_exception()
        finally:
            self.loading_all_chats = False


class CreateChatState(ChatState):

    loading_sending_message: bool

    @rx.var
    def is_group_chat(self) -> bool:
        return True if len(self.participants_selected) > 1 else False
    
    def send_message(self, form_data: dict) -> Generator:
        if len(self.participants_selected) == 0:
            return rx.toast.error("Must add at least one participant to chat.")
        
        if len(self.participants_selected) == 1:
            if not form_data["message"]:
                return rx.toast.error("Must enter a message to send.")
            
            # If sending chat to a user you've already created chat with, send to view message
            owned_chats = (
                self.query()
                .table("chats")
                .select("owner, participant_ids, chat_id")
                .eq("owner", self.user["wickpress"]["id"])
                .execute()
            )
            for chat in owned_chats:
                if self.participants_selected[0]["id"] in chat["participant_ids"]:
                    yield rx.redirect(f"/messages/view/{chat["chat_id"]}")
                    yield rx.toast.info("Existing chat with user found.")

            try:
                new_chat = ChatFull.from_dict({
                    "chat_id": str(uuid.uuid4()),
                    "chat_details": {
                        "name": "",
                        "description": ""
                    },
                    "owner": self.user["wickpress"]["id"],
                    "owner_handle": self.user["wickpress"]["handle"],
                    "created_at": str(datetime.now(timezone.utc).isoformat(timespec="seconds")),
                    "permissions": {
                        "allow_chat": True,
                        "allow_interactions": True,
                        "allow_invites": True
                    },
                    "participant_ids": [self.participants_selected[0]["id"]],
                    "moderator_ids": [],
                    "messages": [
                        {
                            "user_id": self.user["wickpress"]["id"],
                            "content": form_data["message"],
                            "timestamp": str(datetime.now(timezone.utc).isoformat(timespec="seconds")),
                            "interactions": {}
                        }
                    ],
                    "hash": ""
                })
                new_chat.hash_self()
                (
                    self.query()
                    .table("chats")
                    .insert(new_chat.to_dict(), return_="minimal")
                    .execute()
                )
            except Exception as e:
                console.log(f"Issue creating new chat {str(e)}")
                console.print_exception()

        if len(self.participants_selected) > 1:
            if not form_data["group_name"]:
                return rx.toast.error("Must provide a group name for chat.")
            if not form_data["message"]:
                return rx.toast.error("Must enter a message to send.")
            
            try:
                new_chat = ChatFull.from_dict({
                    "chat_id": str(uuid.uuid4()),
                    "chat_details": {
                        "name": form_data.get("group_name", ""),
                        "description": form_data.get("group_description", "")
                    },
                    "owner": self.user["wickpress"]["id"],
                    "owner_handle": self.user["wickpress"]["handle"],
                    "created_at": str(datetime.now(timezone.utc).isoformat(timespec="seconds")),
                    "permissions": {
                        "allow_chat": True,
                        "allow_interactions": True,
                        "allow_invites": True
                    },
                    "participant_ids": [participant["id"] for participant in self.participants_selected],
                    "moderator_ids": [],
                    "messages": [
                        {
                            "user_id": self.user["wickpress"]["id"],
                            "content": form_data["message"],
                            "timestamp": str(datetime.now(timezone.utc).isoformat(timespec="seconds")),
                            "interactions": {}
                        }
                    ],
                    "hash": ""
                })
                new_chat.hash_self()
                (
                    self.query()
                    .table("chats")
                    .insert(new_chat.to_dict(), return_="minimal")
                    .execute()
                )
            except Exception as e:
                console.log(f"Issue creating new chat {str(e)}")
                console.print_exception()


          

class ViewChatState(ChatState):

    CHAT_TIMEOUT_INTERVAL_SEC = 5

    chat_cache: dict[str, ChatFull]
    current_chat: ChatFull
    user_message: str
    last_submitted_message: int
    loading_single_chat: bool

    @rx.var(cache=False, backend=True)
    def chat_is_open(self) -> bool:
        if self.router_data.get("query"):
            if self.router_data["query"]["chat_id_from_url"]:
                console.log("Chat is open.")
                return True
            else:
                return False
        else:
            return False

    def load_single_chat(self) -> EventSpec | None:
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
            cached_chat = self.chat_cache[chat_id_from_url]
            db_chat_hash = (
                self.query()
                .table("chats")
                .select("hash")
                .eq("chat_id", chat_id_from_url)
                .execute()[0]["hash"]
            )
            # Set cached chat to state instead of making db call if current with db
            if cached_chat.hash == db_chat_hash:
                self.current_chat = self.chat_cache[chat_id_from_url]
                console.log(
                    f"Loaded {chat_id_from_url} from [bold red]cache[/bold red] for {self.user["wickpress"]["handle"]}"
                )
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
            sorted_messages = sorted(
                chat["messages"], 
                key=lambda msg: datetime.fromisoformat(msg['timestamp'])
            )            
            # Load object into state
            chat_obj = ChatFull(
                chat_id = chat["chat_id"],
                chat_details = chat["chat_details"],
                owner = chat["owner"],
                created_at = chat["created_at"],
                permissions = chat["permissions"],
                participant_ids = chat["participant_ids"],
                moderator_ids = chat["moderator_ids"],
                messages = sorted_messages,
                hash=chat["hash"]
            )
            self.current_chat = chat_obj
            # Save object under it's own chat id
            self.chat_cache[chat_obj.chat_id] = chat_obj
            console.log(
                f"Loaded {chat_id_from_url} from [bold red]database[/bold red] for {self.user["wickpress"]["handle"]}"
            )
        except Exception as e:
            console.print(str(e))
        finally:
            self.loading_single_chat = False

    def send_message(self, form_data: dict) -> None:
        if not form_data["user_message"]:
            return

        # User can't submit messages within 5 seconds
        current_time = int(time.time())
        if self.last_submitted_message and current_time - self.last_submitted_message < 5:
            return rx.toast.error("Please wait 5 ")

        message = {
            "user_handle": self.user["wickpress"]["handle"],
            "user_id": self.user["wickpress"]["id"],
            "message_id": str(uuid.uuid4()),
            "content": form_data["user_message"],
            "timestamp": str(datetime.now(timezone.utc).isoformat(timespec="seconds"))
        }
        
        # Store the state before our optimistic update, in case of total failure
        original_messages_for_rollback = deepcopy(self.current_chat.messages)
        original_hash_for_rollback = self.current_chat.hash

        for attempt in range(MAX_RETRIES):
            try:
                if attempt == 0:
                    expected_hash = original_hash_for_rollback
                    self.current_chat.messages.append(message)
                    messages_to_update = deepcopy(self.current_chat.messages)
                if attempt > 0:
                    expected_hash = self.current_chat.hash
                    self.current_chat.messages.append(message)
                    messages_to_update = deepcopy(self.current_chat.messages)

                new_hash = self.current_chat.to_hash()

                result = (
                    self.query()
                    .rpc(
                        "update_chat_messages",
                        {
                            "chat_id_to_update": self.current_chat.chat_id,
                            "new_messages": messages_to_update,
                            "new_hash": new_hash,
                            "expected_hash": expected_hash,
                        },
                    )
                    .execute()
                )
                if result:
                    console.log(
                        f"Sent message {message['message_id']} to {self.current_chat.chat_id} on attempt {attempt + 1}"
                    )
                    self.last_submitted_message = current_time
                    self.current_chat.hash = new_hash
                    return
                else:
                    console.log(
                        f"Stale chat in state. Retrying message removal - {attempt +1} of {MAX_RETRIES} retries"
                    )
                    self.load_single_chat()
                    time.sleep(0.5)

            except Exception as e:
                console.print(f"An unexpected error occurred on attempt {attempt + 1}: {e}")
                console.print_exception()
                break

        # When loop finishes after MAX_RETRIES without success
        console.log(
            "Attempts to send message failed. Reverting to previous state."
        )
        self.current_chat.messages = original_messages_for_rollback
        self.current_chat.hash = original_hash_for_rollback

    def remove_message(self, message: dict) -> None:
        if not message["user_id"] == self.user["wickpress"]["id"]:
            return
        
        # Store state before optimistic update, in case of total failure
        original_messages_for_rollback = deepcopy(self.current_chat.messages)
        original_hash_for_rollback = self.current_chat.hash
        
        for attempt in range(MAX_RETRIES):
            try:
                if attempt == 0:
                    expected_hash = original_hash_for_rollback
                    self.current_chat.messages.remove(message)
                    messages_to_update = deepcopy(self.current_chat.messages)
                if attempt > 0:
                    expected_hash = self.current_chat.hash
                    self.current_chat.messages.remove(message)
                    messages_to_update = deepcopy(self.current_chat.messages)
                
                new_hash = self.current_chat.to_hash()

                result = (
                    self.query()
                    .rpc(
                        "update_chat_messages",
                        {
                            "chat_id_to_update": self.current_chat.chat_id,
                            "new_messages": messages_to_update,
                            "new_hash": new_hash,
                            "expected_hash": expected_hash,
                        },
                    )
                    .execute()
                )
                if result:
                    console.log(
                        f"Removed message {message['message_id']} from {self.current_chat.chat_id} on attempt {attempt + 1}"
                    )
                    self.current_chat.hash = new_hash
                    return
                else:
                    console.log(
                        f"Stale chat in state. Retrying message removal - {attempt +1} of {MAX_RETRIES} retries"
                    )
                    self.load_single_chat()
                    time.sleep(0.5)

            except Exception as e:
                console.print(f"An unexpected error occurred on attempt {attempt + 1}: {e}")
                console.print_exception()
                break

        # When loop finishes after MAX_RETRIES without success
        console.log(
            "Attempts to remove message failed. Reverting to previous state"
        )
        self.current_chat.messages = original_messages_for_rollback
        self.current_chat.hash = original_hash_for_rollback
