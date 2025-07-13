
import reflex as rx

from ..components import navbar, navbar_side
from ..states.base import BaseState

@rx.page(
    route="/home",
    title="Home - Wick Press"
)
def home() -> rx.Component:
    return rx.flex(
        rx.flex(
            navbar_side(),
            display=["none", "none", "flex", "flex", "flex"],
        ),
        rx.flex(
            navbar(),
            background_color="var(--gray-1)",
            flex_direction="column",
            flex_grow="1",
            width="100%",
        ),
        flex_direction="row",
        min_height="100vh",
        width="100%",
    )