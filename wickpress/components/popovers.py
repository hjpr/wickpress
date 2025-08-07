
import reflex as rx

from ..states.message import MessageState

def message_recipient_popover() -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.flex(
                rx.text_field(
                    rx.text_field.slot(
                        rx.cond(
                            MessageState.is_loading_recipients,
                            rx.spinner()
                        ),
                        side="right"
                    ),
                    value=MessageState.recipient,
                    id="recipient",
                    placeholder="To",
                    max_length=30,
                    border="1px solid var(--gray-3)",
                    box_shadow="none",
                    width="100%",
                    on_key_down=MessageState.set_is_loading_recipients(True).throttle(200),
                    on_change=MessageState.set_recipient.debounce(200),
                ),
                width="100%"
            )
        ),
        rx.popover.content(
            rx.flex(
                # If recipients available, list retrieved handles
                rx.cond(
                    MessageState.recipients_available,
                    rx.foreach(MessageState.recipients_available, render_recipient),
                    rx.center(
                        rx.text(
                            f'No results for "@{MessageState.no_recipient}"',
                            size="2"
                        )
                    )
                ),
                width="100%"
            ),
            on_open_auto_focus=rx.prevent_default
        ),
        open=MessageState.recipient_popup_is_open,
    )

def render_recipient(recipient: dict) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text(f"@{recipient.get("handle")}"),
            rx.icon("ghost"),
            justify_content="space-between",
            gap="0.5rem"
        ),
        cursor="pointer",
        width="100%",
        on_click=MessageState.add_recipient(recipient)
    )