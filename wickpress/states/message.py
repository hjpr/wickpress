
import reflex as rx
import time

from rich.console import Console
from typing import Callable, Iterable

from ..states.user import UserState

console = Console()

MESSAGE_REFRESH_RATE = 20 # (Interval after which another refresh is allowed - seconds)
MESSAGE_SEND_LIMIT_RATE = 10 # (Interval after which user can send another message - seconds)

class MessageState(UserState):

    """
    Message structure:
        "owner": Message created by uuid
        "owner_handle": User
        "recipient": Intended user's uuid
        "recipient_handle":
        "content": {
            "subject": Message subject,
            "body": Message body,
            "style": Prebuilt message style designator
        },
        "tags": {
            "read": bool,
            "unread": bool,
            "starred": bool,
            "trash": bool
        },
        "created_at" Message created timestamp
        "deleted_at": Message deleted timestamp
    """
    selected_filter: str = "All"
    messages: list[dict[str, dict[str, str]]]
    last_retrieved_unix_timestamp: int
    last_sent_message_unix_timestamp: int
    
    show_new_message_modal: bool = False

    recipient: str
    recipient_list: list[str]
    find_message_recipients_is_open: bool
    recipient_valid: bool
    subject: str
    body: str

    def set_recipient(self, recipient: str) -> Iterable[Callable]:
        self.recipient = recipient
        if not self.find_message_recipients_is_open:
            if recipient:
                self.find_message_recipients_is_open = True
        if self.find_message_recipients_is_open:
            if not recipient:
                self.find_message_recipients_is_open = False

    def retrieve_messages(self) -> Iterable[Callable]:
        """
        Retrieve messages from the database or API. Limits calls to every 60 seconds
        """
        yield MessageState.setvar("is_loading", True)
        current_unix_time = int(time.time())

        # Don't retrieve messages if MESSAGE_REFRESH_RATE hasn't elapsed in seconds
        if self.last_retrieved_unix_timestamp:
            if self.last_retrieved_unix_timestamp + MESSAGE_REFRESH_RATE >= current_unix_time:
                console.print(
                    f"Too early to refresh - {self.last_retrieved_unix_timestamp} + {MESSAGE_REFRESH_RATE} >= {current_unix_time}"
                )
                yield MessageState.setvar("is_loading", False)
                return
        try:
            # Pull messages down by handle
            recieved_messages = (
                self.query()
                .admin()
                .table("messages")
                .select('*')
                .eq("recipient_handle", self.user.get("wickpress", {}).get("handle", ""))
                .execute()
            )
            console.print(recieved_messages)
            yield MessageState.setvar("last_retrieved_unix_timestamp", int(time.time()))
            yield MessageState.setvar("messages", recieved_messages)
            yield MessageState.setvar("is_loading", False)
        except Exception:
            console.print_exception()
            yield rx.toast.error("Issue loading messages")
            yield MessageState.setvar("is_loading", False)

    def send_message(self, form_data: dict) -> Iterable[Callable]:
        """
        Sends a message to a user.
        """
        yield MessageState.setvar("is_loading", True)
        recipient_handle = form_data.get("recipient")
        content = {
            "subject": form_data.get("subject"),
            "body": form_data.get("body")
        }
        try:
            # Check if all content is present
            if not recipient_handle:
                return rx.toast.error("Must specify a user to send message to.")
            if not content.get("subject"):
                return rx.toast.error("Must include a subject line.")
            if not content.get("body"):
                return rx.toast.error("Must contain a message body.")
            
            # Check if recipient is valid by checking if there's a handle that matches
            recipient_valid = (
                self.query()
                .admin()
                .table("profiles")
                .select("*")
                .eq("handle", recipient_handle)
                .execute()
            )
            if not recipient_valid[0]:
                return rx.toast.error(f"{recipient_valid[0]} either doesn't exist, or doesn't accept direct messages.")

            # Upload message to the database.
            (
                self.query()
                .table("messages")
                .insert(
                    {
                        "owner": self.user["wickpress"]["id"],
                        "owner_handle": self.user["wickpress"]["handle"],
                        "recipient_handle": recipient_handle,
                        "content": content
                    }
                )
                .execute()
            )
            yield rx.toast.info("Sent message successfully.")
        except:
            console.print_exception()
            yield rx.toast.error("Issue sending message")
        finally:
            yield MessageState.setvar("is_loading", False)
