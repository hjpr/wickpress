
import httpx
import reflex as rx
import time

from rich.console import Console
from typing import Callable, Iterable

from ..states.user import UserState

console = Console()

MESSAGE_REFRESH_RATE = 10 # (Interval after which another refresh is allowed - seconds)
MESSAGE_SEND_LIMIT_RATE = 10 # (Interval after which user can send another message - seconds)

class MessageState(UserState):

    """
    Message structure:
        "sender": Message created by uuid
        "sender_handle": User
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
    is_loading_recipients: bool

    selected_filter: str = "All"
    messages: list[dict[str, dict[str, str]]]
    last_retrieved_unix_timestamp: int
    last_sent_message_unix_timestamp: int
    

    show_new_message_modal: bool = False

    recipient: str
    no_recipient: str
    recipients_available: list[dict[str, str]]
    recipients_selected: list[dict[str, str]]
    subject: str
    body: str

    @rx.var
    def recipient_popup_is_open(self) -> bool:
        return True if self.recipient else False

    def set_recipient(self, recipient:str) -> Iterable[Callable]:
        self.recipient = recipient
        if len(recipient) > 0:
            self.query_recipient(recipient)
        else:
            self.recipient = ""
            self.no_recipient = ""
            self.is_loading_recipients = False

    def query_recipient(self, recipient: str) -> None:
        # Fire off a search based on the user supplied recipient.
        try:
            valid_recipients = (
                self.query()
                .admin()
                .table("profiles")
                .select("*")
                .ilike("handle", f"{recipient}%")
                .limit(10)
                .execute()
            )
            self.recipients_available = valid_recipients
            # Prevents UI delay from showing a valid search as invalid for a brief second
            if not valid_recipients:
                self.no_recipient = self.recipient
        except:
            console.print_exception()
        finally:
            self.is_loading_recipients = False

    def add_recipient(self, recipient_to_add: dict) -> None:
        self.recipient = ""
        if recipient_to_add not in self.recipients_selected:
            self.recipients_selected.append(recipient_to_add)

    def remove_recipient(self, recipient_to_remove: dict) -> None:
        new_recipient_list = []
        for recipient in self.recipients_selected:
            if recipient["handle"] != recipient_to_remove["handle"]:
                new_recipient_list.append(recipient)
        self.recipients_selected = new_recipient_list

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

    def send_message(self) -> Iterable[Callable]:
        """
        Sends a message to a user.
        """
        self.is_loading = True
        content = {
            "subject": self.subject,
            "body": self.body
        }
        try:
            # Check if all content is present
            if not self.recipients_selected:
                return rx.toast.error("Must specify user(s) to send message to.")
            if not content.get("subject"):
                return rx.toast.error("Must include a subject line.")
            if not content.get("body"):
                return rx.toast.error("Must contain a message body.")

            # Upload message to the database.
            for recipient in self.recipients_selected:
                (
                    self.query()
                    .table("messages")
                    .insert(
                        {
                            "sender": self.user["wickpress"]["id"],
                            "sender_handle": self.user["wickpress"]["handle"],
                            "recipient_handle": recipient["handle"],
                            "content": content
                        }
                    )
                    .execute()
                )
            yield rx.toast.info(f"Sent successfully.")
        except:
            console.print_exception()
            yield rx.toast.error("Issue sending message")
        finally:
            self.recipient = ""
            self.recipients_selected = []
            self.subject = ""
            self.body = ""
            self.show_new_message_modal = False
            self.is_loading = False
