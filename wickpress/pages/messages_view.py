
from statistics import variance
import reflex as rx

from ..components.chat import slim_message
from ..components.modals import new_message_modal
from ..components.nav_bars import navbar, navbar_side
from ..components.protected import login_protected
from ..states.chat import ChatState, ViewChatState


@rx.page(
    route="/messages/view/[chat_id_from_url]",
    title="Messages - Wick Press",
    on_load=ViewChatState.load_single_chat # type: ignore
)
@login_protected
def view() -> rx.Component:
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
                    message_pane(),
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
        bg="var(--gray-5)",
        flex_direction="column",
        height="100vh",
        width="100%",
    )

def message_pane() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.heading(
                        "Fantasy Island Romance Throuple Episodic Content Chat ",
                        size="4",
                        text_overflow="ellipsis",
                        overflow="hidden",
                        white_space="nowrap",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("ellipsis-vertical", size=16),
                        variant="ghost"
                    ),
                    align="center",
                    border_bottom="1px solid var(--gray-3)",
                    padding="1rem",
                    width="100%"
                ),

                # Display chat message area
                rx.flex(
                    rx.scroll_area(
                        rx.flex(
                            rx.foreach(ViewChatState.current_chat.messages, render_message),
                            flex_direction="column",
                            gap="0.5rem",
                            width="100%",
                        )
                    ),
                    flex_grow="1",
                    padding="1rem 1rem 0.5rem 1rem",
                    width="100%",
                    height="0rem",
                ),

                # User entered message
                rx.form(
                    rx.flex(
                        rx.text_area(
                            placeholder="Message",
                            name="user_message",
                            rows="4",
                            width="100%"
                        ),
                        rx.button(
                            rx.icon("send", size=16),
                            type="submit",
                            cursor="pointer"
                        ),
                        gap="1rem",
                        padding="0.5rem 1rem 1rem 1rem",
                        width="100%"
                    ),
                    on_submit=ViewChatState.send_message,
                    reset_on_submit=True
                ),
                bg="var(--gray-2)",
                flex_direction="column",
                flex_grow="1",
                border="1px solid var(--gray-4)",
                border_radius = "0.75rem",
                scroll_margin_top="10rem",  # Ensure content is not hidden behind sticky navbar and filters
                width='100%',
            ),
            flex_direction="column",
            flex_grow="1",
            gap="1rem",
            max_width="36rem",
            width="100%"
        ),
        bg="var(--gray-3)",
        flex_direction="column",
        flex_grow="1", 
        align="center", # Center content horizontally
        padding=rx.breakpoints(
            xs="5.5rem 1rem 1rem 1rem", # When sidebar is hidden
            sm="5.5rem 1rem 1rem 4.5rem",
            md="5.5rem 1rem 1rem 4.5rem", 
            lg="5.5rem 1rem 1rem 4.5rem", 
            xl="5.5rem 1rem 1rem 4.5rem" 
        )
    )

def render_message(message: dict) -> rx.Component:
    return rx.hover_card.root(
        rx.hover_card.trigger(
            rx.flex(
                rx.text(
                    f"@{message['user_handle']}",
                    size="2",
                    color="var(--gray-9)",
                    cursor="pointer",
                    _hover={
                        "text-decoration": "underline"
                    }
                ),
                rx.flex(
                    rx.text(
                        message["content"],
                        size="2"
                    ),
                    padding="0rem 1rem"
                ),
                flex_direction="column",
                width="100%",
            )
        ),
        rx.hover_card.content(
            rx.button(
                rx.icon("pencil", size=16),
                variant="soft",
                cursor="pointer"
            ),
            rx.popover.root(
                rx.popover.trigger(
                    rx.button(
                        rx.icon("ellipsis", size=16),
                        variant="soft",
                        cursor="pointer"
                    ),
                ),
                rx.popover.content(
                    rx.flex(
                        rx.text("Delete Message", size="2"),
                        rx.icon("trash", size=16),
                        gap="3rem",
                        align="center",
                        padding="0.5rem",
                        border_radius="0.5rem",
                        cursor="pointer",
                        _hover={"bg": "var(--gray-3)"},
                        on_click=ViewChatState.remove_message(message)
                    ),
                    size="1",
                    align="end",
                    side="bottom",
                    border="1px solid var(--gray-4)",
                    box_shadow="none",
                    outline="none",
                    padding="0.5rem"
                )
            ),
            display="flex",
            bg="none",
            size="1",
            side="top",
            align="end",
            side_offset=-20,
            align_offset=0,
            box_shadow="none",
            outline="none",
            gap="0.5rem",
        )
    )