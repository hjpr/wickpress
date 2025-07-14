
import reflex as rx

from ..components import navbar, navbar_side
from ..states.base import BaseState

@rx.page(
    route="/library",
    title="Library - Wick Press"
)
def library() -> rx.Component:
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
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger(
                                "New Releases",
                                value="new_releases",
                                cursor="pointer",
                                width="33%",
                            ),
                            rx.tabs.trigger(
                                "All Content",
                                value="all_content",
                                cursor="pointer",
                                width="34%",
                            ),
                            rx.tabs.trigger(
                                "Subscriptions",
                                value="subscriptions",
                                cursor="pointer",
                                width="33%",
                            ),
                            width="100%",
                        ),
                        rx.tabs.content(
                            new_releases_tab(),
                            flex_grow="1",
                            value="new_releases",
                        ),
                        rx.tabs.content(
                            all_content_tab(),
                            value="all_content",
                        ),
                        rx.tabs.content(
                            subscriptions_tab(),
                            value="subscriptions",
                        ),
                        display="flex",
                        flex_direction="column",
                        flex_grow="1",
                        width="100%",
                    ),
                    width='36rem',
                ),
                justify="center", # Keeps the content centered
                width="100%",
            ),
            background_color="var(--gray-1)",
            flex_direction="column",
            flex_grow="1",
            width="100%",
        ),
        flex_direction="row",
        height="100vh",
        width="100%",
    )

def new_releases_tab() -> rx.Component:
    return rx.flex(
        rx.scroll_area(
            rx.flex(
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                rx.card("New releases will be displayed here..."),
                flex_direction="column",
                gap="1rem",
                width="100%",
            ),
            padding="1rem",
            width="100%",
        ),
    )

def all_content_tab() -> rx.Component:
    return rx.flex(
        rx.callout(
            "All content goes here...",
            padding="1rem",
            width="100%"
        ),
        padding="2rem",
        width="100%",
    )

def subscriptions_tab() -> rx.Component:
    return rx.flex(
        rx.callout(
            "Subscription content goes here...",
            padding="1rem",
            width="100%"
        ),
        padding="2rem",
        width="100%",
    )