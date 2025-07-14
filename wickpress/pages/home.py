
import reflex as rx

from ..components import navbar, navbar_side
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
                padding="5.5rem 1rem 1rem 1rem",
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