
import reflex as rx

from ..components import navbar, navbar_side
from ..states.base import BaseState

@rx.page(
    route="/library",
    title="Library - Wick Press"
)
def library() -> rx.Component:
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
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger(
                                "New Releases",
                                value="new_releases",
                                cursor="pointer",
                                width="33%",
                                on_click=rx.scroll_to(elem_id="new_releases")
                            ),
                            rx.tabs.trigger(
                                "All Content",
                                value="all_content",
                                cursor="pointer",
                                width="34%",
                                on_click=rx.scroll_to(elem_id="all_content")
                            ),
                            rx.tabs.trigger(
                                "Subscriptions",
                                value="subscriptions",
                                cursor="pointer",
                                width="33%",
                                on_click=rx.scroll_to(elem_id="subscriptions")
                            ),
                            bg="var(--gray-1)",
                            position="sticky",
                            top="4.5rem",
                            width="100%",
                            z_index="10",
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
                        default_value="new_releases",
                        display="flex",
                        flex_direction="column",
                        flex_grow="1",
                        width="100%",
                    ),
                    flex_direction="column",
                    flex_grow="1",
                    max_width='36rem',
                    width='100%',
                ),
                flex_direction="column",
                align="center",
                padding=rx.breakpoints(
                    xs="4.5rem 0 0 0",  # When sidebar is hidden
                    sm="4.5rem 0 0 4.5rem",
                    md="4.5rem 0 0 4.5rem",
                    lg="4.5rem 0 0 4.5rem",
                    xl="4.5rem 0 0 4.5rem",
                ),
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

def new_releases_tab() -> rx.Component:
    return rx.flex(
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        id="new_releases",
        flex_direction="column",
        scroll_margin_top="10rem",
        width="100%",
        class_name="divide-y divide-[var(--gray-3)]",
    )

def all_content_tab() -> rx.Component:
    return rx.flex(
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        id="all_content",
        flex_direction="column",
        scroll_margin_top="10rem",
        width="100%",
        class_name="divide-y divide-[var(--gray-3)]",
    )

def subscriptions_tab() -> rx.Component:
    return rx.flex(
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        id="subscriptions",
        flex_direction="column",
        scroll_margin_top="10rem",
        width="100%",
        class_name="divide-y divide-[var(--gray-3)]",
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