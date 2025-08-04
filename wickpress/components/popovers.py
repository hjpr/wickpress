
import reflex as rx

from ..states.message import MessageState

def message_recipient_popover() -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.flex(
                rx.text_field(
                    value=MessageState.recipient,
                    id="recipient",
                    placeholder="To",
                    border="1px solid var(--gray-3)",
                    box_shadow="none",
                    width="100%",
                    on_change=MessageState.set_recipient.debounce(300)
                ),
                width="100%"
            )
        ),
        rx.popover.content(
            rx.center(
                rx.spinner(),
            ),
            on_open_auto_focus=rx.prevent_default
        ),
        open=MessageState.find_message_recipients_is_open,
    )