
import reflex as rx

from ..components import navbar, navbar_side
from ..states.base import BaseState

@rx.page(
    route="/messages",
    title="Messages - Wick Press"
)
def messages() -> rx.Component:
    return rx.flex(
        rx.flex(
            navbar_side(),
            display=["none", "none", "flex", "flex", "flex"],
        ),
        rx.flex(
            navbar(),
            # Content area for the main page
            rx.flex(
                rx.flex(
                    max_width='36rem',
                ),
                height="100%",
                justify="center",
                width="100%",
            ),
            background_color="var(--gray-1)",
            flex_direction="column",
            flex_grow="1",
            width="100%",
        ),
        flex_direction="row",
        min_height="100vh",
        width="100%",
    )