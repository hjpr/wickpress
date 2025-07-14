
import reflex as rx

from ..components.nav_bars import navbar, navbar_side
from ..components.nav_panel import nav_panel
from ..states.base import BaseState

discover_filters: list[str] = [
    "Trending",
    "New Releases",
    "Popular",
    "Short Stories",
    "Upcoming",
    "Editor's Picks",
    "Most Read",
    "Most Shared",
    "Cyberpunk",
    "Fantasy",
    "Science Fiction",
    "Horror",
    "Romance",
    "Mystery",
    "Thriller",
]

@rx.page(
    route="/discover",
    title="Discover - Wick Press"
)
def discover() -> rx.Component:
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
                    nav_panel(discover_content(), discover_filters),
                    flex_direction="column",
                    flex_grow="1",
                    width='100%',
                ),
                flex_direction="column",
                align="center",
                width="100%",
            ),
            background_color="var(--gray-1)",
            flex_direction="row",
            flex_grow="1",
            width="100%",
        ),
        flex_direction="column",
        height="100vh",
        width="100%",
    )

def discover_content() -> rx.Component:
    return rx.flex(
        rx.text("Discover content goes here."),
        border="1px solid black",
        flex_direction="column",
        flex_grow="1",
        padding="1rem",
    )

def mockup_element_post() -> rx.Component:
    return rx.flex(
        # Profile picture container
        rx.flex(
            rx.skeleton(
                height="3rem",
                width="3rem",
                border_radius="full",
            ),
            flex_direction="column",
            justify="start",
        ),
        # Element content container
        rx.flex(
            rx.skeleton(
                height="1.5rem",
            ),
            rx.skeleton(
                height="5.5rem",
            ),
            rx.skeleton(
                height="1.5rem",
            ),
            flex_direction="column",
            flex_grow="1",
            gap="1rem",
            padding="0 1rem"
        ),
        flex_direction="row",
        flex_grow="1",
        padding="1.25rem 1rem",
    )