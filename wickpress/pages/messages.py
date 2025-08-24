
from turtle import width
import reflex as rx

from ..classes.chat import ChatPartial
from ..components.nav_bars import navbar, navbar_side
from ..components.protected import login_protected
from ..states.chat import ChatState
from ..states.page import PageState

messages_filters: list[str] = [
    "All",
    "Unread",
    "Read",
    "Sent",
    "Starred",
    "Trash",
]

@rx.page(
    route="/messages",
    title="Messages - Wick Press",
    on_load=ChatState.load_all_chats
)
@login_protected
def messages() -> rx.Component:
    return rx.flex(
        navbar(),

        # Contains side navigation and main content
        rx.flex(

            # Sidebar for navigation
            navbar_side(),

            # Main content container
            rx.flex(

                # Main content area, centered and width-limited
                rx.flex(

                    # Panel with header and filters
                    nav_panel_messages(
                        chat_content(),
                        messages_filters,
                        overflow=False,
                        sticky=True
                    ),
                    flex_direction="column",
                    flex_grow="1",
                    width='100%',
                ),
                flex_direction="column",
                align="center",
                width="100%",
            ),
            flex_direction="row",
            flex_grow="1",
            width="100%",
        ),
        flex_direction="column",
        height="100vh",
        width="100%",
    )

def nav_panel_messages(
        content: rx.Component,
        filters: list[str],
        overflow: bool = False,
        sticky: bool = True
        ) -> rx.Component:
    return rx.flex(

        # Main content area
        rx.flex(
            rx.flex(
                rx.heading(ChatState.selected_filter),

                # Messages header and buttons
                rx.flex(
                    rx.button(
                        rx.icon("pen", size=16),
                        rx.text("Create"),
                        cursor="pointer",
                        on_click=[
                            ChatState.set_participant(""),
                            ChatState.set_participants_selected([]),
                            rx.redirect("/messages/create")
                        ]
                    ),
                    rx.button(
                        rx.icon("ellipsis", size=16),
                        variant="soft",
                        cursor="pointer"
                    ),
                    gap="0.5rem"
                ),
                align="center",
                bg="var(--gray-1)",
                padding="1rem",
                border_bottom="1px solid var(--gray-3)",
                top="4.5rem",
                justify_content="space-between",
                user_select="none",
            ),

            # Filters
            rx.cond(
                overflow,
                # Horizontally scrolling container for filters that overflow
                rx.flex(
                    rx.flex(
                        rx.icon("chevron_left", color="var(--gray-10)"),
                        background_image="linear-gradient(to right, var(--gray-1), var(--gray-1) 60%, transparent)",
                        flex_shrink="0",
                        cursor="pointer",
                        align="center",
                        justify="center", 
                        height="3rem",
                        width="4rem",
                        padding="0 1.5rem 0 0",
                        position="absolute",
                        on_click=rx.call_script(
                            "document.getElementById('nav-filter-container').scrollBy({ left: -350, behavior: 'smooth' })",
                            callback=PageState.default_script_callback
                        ),
                    ),
                    rx.flex(
                        rx.foreach(filters, filter_element),
                        id="nav-filter-container",
                        flex_direction="row",
                        flex_grow="1",
                        gap="1rem",
                        height="3rem",
                        padding="0 3.25rem",
                        align="center",
                        overflow_x="scroll",
                        scrollbar_width="none"
                    ),
                    rx.flex(
                        rx.icon("chevron_right", color="var(--gray-10)"),
                        background_image="linear-gradient(to left, var(--gray-1), var(--gray-1) 60%, transparent)",
                        flex_shrink="0",
                        cursor="pointer",
                        align="center",
                        justify="center", 
                        height="3rem",
                        width="4rem",
                        padding="0 0 0 1.5rem",
                        position="absolute",
                        right="0",
                        on_click=rx.call_script(
                            "document.getElementById('nav-filter-container').scrollBy({ left: 350, behavior: 'smooth' })",
                            callback=PageState.default_script_callback
                        ),
                    ),
                    flex_direction="row",
                    position="relative",
                    max_width="44rem",
                    width="100%",
                ),
                # Horizontally scrolling container for filters that DO NOT overflow
                rx.flex(
                    rx.flex(
                        rx.foreach(filters, filter_element),
                        id="nav-filter-container",
                        flex_direction="row",
                        flex_grow="1",
                        gap="1rem",
                        height="3rem",
                        align="center",
                        justify="center",
                        padding_left="0.25rem",
                        overflow_x="scroll",
                        scrollbar_width="none"
                    ),
                    bg="var(--gray-1)",
                    flex_direction="row",
                    position="sticky" if sticky else "relative",
                    top="4.5rem" if sticky else "0",
                    padding="0rem 1rem",
                    border_bottom="1px solid var(--gray-3)",
                    max_width="36rem",
                    width="100%",
                ),
            ),

            # Displayed messages
            content,

            id="messages-content",
            flex_direction="column",
            flex_grow="1",
            max_width='36rem',
            scroll_margin_top="10rem",  # Ensure content is not hidden behind sticky navbar and filters
            width='100%',
        ),
        bg="var(--gray-1)",
        flex_direction="column",
        flex_grow="1", 
        align="center", # Center content horizontally
        padding=rx.breakpoints(
            xs="4.5rem 0 0 0", # When sidebar is hidden
            sm="4.5rem 0 0 4.5rem",
            md="4.5rem 0 0 4.5rem", 
            lg="4.5rem 0 0 4.5rem", 
            xl="4.5rem 0 0 4.5rem" 
        )
    )

def filter_element(filter: str) -> rx.Component:
    return rx.flex(
        rx.badge(
            filter,
            cursor="pointer",
            size="3",
            user_select="none",
            class_name=rx.cond(
                ChatState.selected_filter == filter,
                "ring-3 ring-[var(--gray-6)]",
                ""
            ),
            on_click=[
                ChatState.setvar("selected_filter", filter),  # Update selected filter state
                rx.scroll_to(elem_id="messages-content")  # Scroll to messages content
            ]
        ),
        cursor="pointer"
    )

def chat_content() -> rx.Component:
    return rx.flex(
        rx.cond(
            # If loading, show skeletons
            ChatState.is_loading,
            rx.flex(
                rx.spinner(),
                flex_direction="column",
                flex_grow="1",
            ),

            # If there are messages, display, otherwise empty icon
            rx.flex(
                rx.cond(
                    ChatState.chats,
                    rx.foreach(
                        ChatState.chats,
                        render_message
                    ),
                    rx.flex(
                        rx.center(
                            rx.text(
                                f'No messages in "{ChatState.selected_filter}"',
                                size="3",
                                color="var(--gray-6)"
                            ),
                        ),
                        flex_direction="row",
                        justify="center",
                        padding="8rem"
                    )
                ),

                # Pagination controls and number
                rx.flex(
                    border_bottom="1px solid var(--gray-3)",
                    width="100%"
                ),
                flex_direction="column",
                flex_grow="1",
            ),
        ),
        flex_direction="column",
        flex_grow="1",
    )

def render_message(chat: ChatPartial) -> rx.Component:
    return rx.flex(
        # Profile picture container
        rx.flex(
            rx.flex(
                rx.cond(
                    chat.is_group_chat,
                    rx.icon("users"),
                    rx.icon("user"),
                ),
                align="center",
                justify="center",
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
                rx.cond(
                    chat.is_group_chat,
                    rx.text(
                        f"Group Chat: {chat.chat_details["name"]}",
                        text_overflow="ellipsis",
                        overflow="hidden",
                        white_space="nowrap",
                    ),
                ),
                rx.flex(
                    rx.cond(
                        ~chat.is_group_chat,
                        rx.text(
                            f"Private Chat"
                        ),
                    ),
                    rx.text(
                        f"@{chat.owner_handle}",
                        size="2"
                    ),
                    flex_direction="column"
                ),
                justify="center",
                flex_direction="column",
                flex_grow="1",
                width="100%"
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