
import reflex as rx
import time

from rich.console import Console
from typing import Callable, Iterable

from ..states.user import UserState

console = Console()

MESSAGE_REFRESH_RATE = 60 # (Interval after which another refresh is allowed - seconds)
MESSAGE_SEND_LIMIT_RATE = 10 # (Interval after which user can send another message - seconds)

class MessageState(UserState):

    """
    Message structure:
        "id": Message created by uuid
        "recipient": Intended user's uuid
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
        "deleted_at": Message deleted timestamp
    """
    messages: list[dict[str, dict[str, str]]]
    last_retrieved_unix_timestamp: float
    last_sent_message_unix_timestamp: float
    
    selected_filter: str = "All"
    show_new_message_modal: bool = False

    def retrieve_messages(self) -> Iterable[Callable]:
        """
        Retrieve messages from the database or API. Limits calls to every 60 seconds
        """
        current_unix_time = time.time()
        if (
            self.last_retrieved_unix_timestamp 
            or self.last_retrieved_unix_timestamp + MESSAGE_REFRESH_RATE <= current_unix_time
        ):
            return
        yield MessageState.setvar("is_loading", True)
        try:
            messages = (
                self.query()
                .select('*')
                .or_(
                    id=f'eq.{self.user["wickpress"]["id"]}',
                    recipient=f'eq.{self.user["wickpress"]["id"]}',
                )
                .execute()
            )
            console.print(messages)
            yield MessageState.setvar("last_retrieved_unix_timestamp")
            yield MessageState.setvar("messages", )
            yield MessageState.setvar("is_loading", False)
        except Exception:
            console.print_exception()
            yield rx.toast.error("Issue loading messages")
            yield MessageState.setvar("is_loading", False)

    def send_message(self, form_data: dict) -> Iterable[Callable]:
        """
        Sends a message to a user.
        """
        console.print(form_data)
        recipient_handle = form_data.get("recipient")
        content = {
            "subject": form_data.get("subject"),
            "body": form_data.get("body")
        }

        console.print(id)
        yield MessageState.setvar("is_loading", True)
        try:
            (
                self.query()
                .table("messages")
                .insert(
                    {
                        "id": self.user["wickpress"]["id"],
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
