
import reflex as rx

from ..classes.chat import ChatPartial
    
def slim_message(chat: ChatPartial) -> rx.Component:
    return rx.flex(
        # Profile picture container
        rx.flex(
            rx.skeleton(
                height="3rem",
                width="3rem",
                border_radius="full",
            ),
            flex_direction="column",
            justify="start",
        ),
        # Content container
        rx.flex(
            rx.flex(
                rx.text(
                    chat.chat_details["name"],
                    text_overflow="ellipsis",
                    overflow="hidden",
                    white_space="nowrap",
                ),
                rx.flex(
                    rx.text(f"@{chat.owner_handle}", size="2")
                ),
                flex_direction="column",
            ),
            flex_direction="column",
            gap="1rem",
            width="100%"
        ),
        display="flex",
        flex_direction="row",
        justify="center",
        gap="1rem",
        border_radius="0.75rem",
        padding="1rem",
        cursor="pointer",
        on_click=rx.redirect(f"/messages/view/{chat['chat_id']}")
    )

def expanded_message(message: dict[str, str]) -> rx.Component:
    return rx.flex()
