
import reflex as rx

from ..components import navbar, navbar_side
from ..states.auth import AuthState
from ..states.base import BaseState

@rx.page(
    route="/home",
    title="Home - Wick Press"
)
def home() -> rx.Component:
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
                    rx.card(
                        flex_grow="1",
                    ),
                    flex_direction="column",
                    flex_grow="1",
                    max_width='36rem',
                    width='100%',
                ),
                flex_direction="column",
                align="center",
                padding=rx.breakpoints(
                    xs="5.5rem 0 0 0",  # When sidebar is hidden
                    sm="5.5rem 0 0 4.5rem",
                    md="5.5rem 0 0 4.5rem",
                    lg="5.5rem 0 0 4.5rem",
                    xl="5.5rem 0 0 4.5rem",
                ),
                width="100%",
            ),
            background_color="var(--gray-1)",
            flex_direction="row",
            flex_grow="1",
            width="100%",
        ),
        flex_direction="column",
        scroll_padding_top="4.5rem",
        height="100vh",
        width="100%",
    )