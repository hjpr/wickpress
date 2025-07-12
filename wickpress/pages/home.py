
import reflex as rx

from ..components import navbar
from ..states.base import BaseState

@rx.page(
    route="/home",
    title="Home - Wick Press"
)
def home() -> rx.Component:
    return rx.flex(
        navbar(),
        rx.flex(
            rx.button(
                "Whats router data.",
                on_click=BaseState.check_router_data,
            )
        ),
        align="center",
        background_color="var(--gray-1)",
        flex_direction="column",
        min_height="100vh",
        padding="4rem 2rem 2rem 2rem",
        width="100%",
    )