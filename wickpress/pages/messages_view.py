
import reflex as rx

from ..components.mail import slim_message
from ..components.modals import new_message_modal
from ..components.nav_bars import navbar, navbar_side
from ..components.protected import login_protected
from ..states.message import MessageState
from ..states.page import PageState


sample_user_message = "Hey, whats up. I heard you farted while you were eating."
sample_participant_message = "ya lol, its nbd. i call it a beef queef." 

@rx.page(
    route="/messages/view/[message_id]",
    title="Messages - Wick Press"
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
                rx.flex(
                    rx.scroll_area(
                        rx.flex(
                            rx.flex(
                                rx.text("@hurgleburglar", size="1"),
                                rx.text(sample_user_message, size="2"),
                                flex_direction="column",
                                width="100%"
                            ),
                            rx.flex(
                                rx.text("@hurgleburglar", size="1"),
                                rx.text(sample_user_message, size="2"),
                                flex_direction="column",
                                width="100%"
                            ),
                            rx.flex(
                                rx.text("@hurgleburglar", size="1"),
                                rx.text(sample_user_message, size="2"),
                                flex_direction="column",
                                width="100%"
                            ),
                            rx.flex(
                                rx.text("@hurgleburglar", size="1"),
                                rx.text(sample_user_message, size="2"),
                                flex_direction="column",
                                width="100%"
                            ),
                            rx.flex(
                                rx.text("@hurgleburglar", size="1"),
                                rx.text(sample_user_message, size="2"),
                                flex_direction="column",
                                width="100%"
                            ),
                            rx.flex(
                                rx.text("@hurgleburglar", size="1"),
                                rx.text(sample_user_message, size="2"),
                                flex_direction="column",
                                width="100%"
                            ),
                            flex_direction="column",
                            gap="1rem",
                            width="100%",
                        )
                    ),
                    flex_grow="1",
                    padding="1rem 1rem 0.5rem 1rem",
                    width="100%",
                    height="0rem",
                ),
                rx.flex(
                    rx.text_area(
                        placeholder="Message",
                        rows="4",
                        width="100%"
                    ),
                    padding="0.5rem 1rem 1rem 1rem",
                    width="100%"
                ),
                bg="var(--gray-2)",
                flex_direction="column",
                flex_grow="1",
                border="1px solid var(--gray-3)",
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
        bg="var(--gray-1)",
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