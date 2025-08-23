
import reflex as rx

from .popovers import message_participant_popover
from ..states.chat import ChatState
from ..states.page import PageState

def search_modal_for_navbar() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.flex(
                rx.button(
                    rx.icon("search", size=18),
                    loading=PageState.is_loading,
                    cursor="pointer",
                    size="1",
                    variant="ghost",
                    _hover={"bg": "none"}
                ),
                align="center",
                justify="center",
                height="100%",
                width='2rem',
            )
        ),
        rx.dialog.content(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.icon(
                            "search",
                            color="var(--gray-11)",
                            size=18
                        ),
                        align="center",
                        justify="center",
                        height="100%",
                        width="3rem",
                    ),
                    rx.flex(
                        rx.text_field(
                            placeholder="Writers, series, episodes, tags...",
                            value=PageState.search_input,
                            bg="none",
                            border="none",
                            box_shadow="none",
                            outline="none",
                            size="3",
                            type="search",
                            width="100%",
                            _focus_within={
                                "outline": "none",
                                "box_shadow": "none"
                            },
                            on_change=PageState.setvar("search_input").debounce(500),
                        ),
                        align="center",
                        width="100%",
                    ),
                    rx.button(
                        rx.text("Cancel"),
                        cursor="pointer",
                        size="2",
                        variant="soft",
                        on_click=[
                            PageState.setvar("search_input", ""),
                            PageState.setvar("search_modal_open", False)
                        ],
                    ),
                    align="center",
                    height="3rem",
                    padding="2rem 1rem 2rem 1rem",
                    position="sticky",
                    top="0",
                    width="100%",
                ),
                rx.separator(
                    z_index="10",
                ),
                rx.scroll_area(
                    skeleton_search_results(),
                    padding="1rem",
                    width="100%",
                ),
                flex_direction="column",
                height="36rem",
            ),
            padding="0 0 0 0",
            on_pointer_down_outside=PageState.setvar("search_modal_open", False),
        ),
        open=PageState.search_modal_open,
    )

def search_results() -> rx.Component:
    return rx.flex(
        # Image placeholder
        rx.flex(
            bg="var(--gray-1)",
            height='3rem',
            width='3rem',
        ),
        # Contains element text
        rx.flex(
            rx.flex(
                rx.text("Element Name", size="3", weight="medium"),
            ),
            rx.flex(
                rx.text("Type", size="2", weight="light"),
                rx.text("-", size="2", weight="light"),
                rx.text("Subgroup", size="2", weight="light"),
                rx.text("-", size="2", weight="light"),
                rx.text("Subscribers", size="2", weight="light"),
                gap="0.5rem",
            ),
            flex_direction="column",
            justify="center",
            padding="0 1rem",
        ),
        border_radius="0.5rem",
        cursor="pointer",
        _hover={
            "bg":"var(--gray-3)",
        },
        padding="1rem",
        width="100%",
    )

def render_trending_topics(topic: dict) -> rx.Component:
    return rx.flex(
        # Image placeholder
        rx.flex(
            rx.icon("trending-up"),
            bg="var(--gray-1)",
            align="center",
            justify="center",
            height='3rem',
            width='3rem',
        ),
        # Contains element text
        rx.flex(
            rx.flex(
                rx.text(f"{topic["name"]}", size="3", weight="medium"),
                align="center",
                justify="center",
                padding="0.25rem 0rem 0rem 0rem"
            ),
            flex_direction="column",
            justify="center",
            padding="0 1rem",
        ),
        border_radius="0.5rem",
        cursor="pointer",
        _hover={
            "bg":"var(--gray-3)",
        },
        padding="1rem",
        width="100%",
    )

def skeleton_search_element() -> rx.Component:
    return rx.flex(
        # Image placeholder
        rx.skeleton(
            height='3rem',
            width='3rem',
        ),
        # Contains element text
        rx.flex(
            rx.skeleton(
                width="100%",
            ),
            rx.skeleton(
                width="100%",
            ),
            gap="0.5rem",
            flex_direction="column",
            justify="center",
            padding="0 1rem",
            width="100%",
        ),
        padding="1rem",
        width="100%",
    )

def skeleton_search_results() -> rx.Component:
    return rx.cond(
        PageState.search_results_not_ready,
        rx.flex(
            skeleton_search_element(),
            skeleton_search_element(),
            skeleton_search_element(),
            skeleton_search_element(),
            skeleton_search_element(),
            skeleton_search_element(),
            flex_direction="column",
        ),
        rx.foreach(
            PageState.trending_topics,
            render_trending_topics
        )
    )

def new_message_modal() -> rx.Component:
    """
    Modal displayed when user wants to send a message to another user.
    """
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("pen", size=16),
                rx.text("Compose"),
                cursor="pointer",
                on_click=ChatState.set_new_chat_modal_open(True)
            ),
        ),
        rx.dialog.content(
            rx.flex(
                rx.flex(
                    rx.button(
                        rx.icon("send", size=18),
                        cursor="pointer",
                        size="2"
                    ),
                    rx.text("Compose New Chat"),
                    rx.button(
                        rx.text("Cancel"),
                        type="button",
                        cursor="pointer",
                        size="2",
                        variant="soft",
                        on_click=ChatState.set_new_chat_modal_open(False)
                    ),
                    align="center",
                    justify="between",
                    padding="1rem",
                    position="sticky",
                    top="0",
                    width="100%",
                ),
                rx.separator(
                    z_index="10",
                ),
                rx.flex(
                    # 'To' field embedded in popover trigger
                    rx.flex(
                        message_participant_popover(),
                        rx.tooltip(
                            rx.button(
                                rx.icon("contact", size=16),
                                variant="soft",
                                cursor="pointer"
                            ),
                            content="Contacts"
                        ),
                        gap="1rem"
                    ),
                    # User selected members for group chat
                    rx.cond(
                        ChatState.participants_selected,
                        rx.flex(
                            rx.foreach(
                                ChatState.participants_selected,
                                participants_selected_render
                            ),
                        ),
                    ),
                    rx.flex(
                        rx.text_area(
                            placeholder="Message",
                            rows="6",
                            size="2",
                            border="1px solid var(--gray-3)",
                            box_shadow="none",
                            width="100%"
                        ),
                        flex_grow="1",
                        width="100%"
                    ),
                    flex_direction="column",
                    flex_grow="1",
                    gap="1rem",
                    padding="1rem",
                    width="100%"
                ),
                flex_direction="column",
            ),
            padding="0 0 0 0",
            on_interact_outside=ChatState.set_new_chat_modal_open(False)
        ),
        open=ChatState.new_chat_modal_open,
    )

def participants_selected_render(participant: dict) -> rx.Component:
    """
    Renders small badge of a selected user to allow into chat.
    """
    return rx.flex(
        rx.text(f"@{participant.get('handle')}", size="2"),
        rx.center(
            rx.icon("x", size=14),
            height="1.25rem",
            width="1.25rem",
            border_radius="calc(infinity * 1px)",
            cursor="pointer",
            _hover={
                "bg": "var(--gray-4)"
            },
            on_click=ChatState.remove_participants(participant)
        ),
        align="center",
        border="1px solid var(--gray-3)",
        border_radius="calc(infinity * 1px)",
        padding="0.25rem 0.5rem",
        gap="0.5rem",
    )