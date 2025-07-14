
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
        rx.flex(

            # Sidebar for navigation
            navbar_side(),

            # Main content area
            rx.flex(
                rx.flex(
                    rx.callout("Fart"),
                    flex_direction="column",
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