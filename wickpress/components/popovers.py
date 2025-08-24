
import reflex as rx

from ..states.chat import ChatState

def message_participant_popover() -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.flex(
                rx.text_field(
                    rx.text_field.slot(
                        rx.cond(
                            ChatState.loading_participants,
                            rx.spinner()
                        ),
                        side="right"
                    ),
                    value=ChatState.participant,
                    placeholder="To",
                    max_length=30,
                    size="2",
                    border="1px solid var(--gray-3)",
                    border_radius="0.75rem",
                    box_shadow="none",
                    width="100%",
                    on_key_down=ChatState.set_loading_participants(True).throttle(100),
                    on_change=ChatState.set_participant.debounce(100),
                ),
                width="100%"
            )
        ),
        rx.popover.content(
            rx.flex(
                # If participants available, list retrieved handles
                rx.cond(
                    ChatState.participants_available,
                    rx.foreach(ChatState.participants_available, render_participant),
                    rx.center(
                        rx.text(
                            f'No results for "@{ChatState.participant}"',
                            size="2"
                        )
                    )
                ),
                width="100%"
            ),
            on_open_auto_focus=rx.prevent_default,
        ),
        open=ChatState.participant_popup_open,
    )

def render_participant(participant: dict) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text(f"@{participant.get("handle")}"),
            rx.icon("ghost"),
            justify_content="space-between",
            gap="0.5rem"
        ),
        cursor="pointer",
        width="100%",
        on_click=ChatState.set_participants_selected(participant)
    )