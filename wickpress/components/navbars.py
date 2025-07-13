import reflex as rx

from reflex.style import toggle_color_mode
from ..states.base import BaseState

def navbar() -> rx.Component:
    return rx.flex(
        # Main navigation bar with logo and buttons.
        rx.flex(
            # Holds logo and buttons.
            rx.flex(
                # Mobile dropdown for navigation.
                rx.drawer.root(
                    rx.drawer.trigger(
                        rx.icon(
                            "menu",
                            size=24,
                            cursor="pointer",
                        ),
                        display=["inline", "inline", "none", "none", "none"],
                    ),
                    rx.drawer.portal(
                        rx.drawer.content(
                            rx.flex(
                                rx.drawer.close(rx.box(rx.button("Close"))),
                            ),
                            height="100%",
                            width="20em",
                            padding="2em",
                            background_color="#FFF",
                        )
                    ),
                    direction="left",
                ),

                rx.flex(
                    # Show publish button only when at the about page.
                    rx.cond(
                        BaseState.current_page == "/about",
                        rx.button(
                            rx.text(
                                "Start writing",
                            ),
                            cursor="pointer",
                            size=rx.breakpoints(
                                initial="2",
                                md="3",
                            )
                        )
                    ),

                    # Search input field only on the home page.
                    rx.cond(
                        BaseState.current_page == "/home",
                        rx.input(
                            placeholder="Search...",
                            width="100%",
                            size=rx.breakpoints(
                                initial="2",
                                md="3",
                            ),
                            display=["none", "flex", "flex", "flex", "flex"],
                        )
                    ),
                    # Search icon on mobile.
                    rx.button(
                        rx.icon(
                            "Search",
                            size=18
                        ),
                        cursor="pointer",
                        display=["inline", "none", "none", "none", "none"],
                        size=rx.breakpoints(initial="2", md="3"),
                        variant="soft",
                    ),

                    rx.button(
                        rx.text(
                            "Sign in",
                            on_click=rx.redirect("/sign-in")
                        ),
                        cursor="pointer",
                        size=rx.breakpoints(
                            initial="2",
                            md="3",
                        ),
                        variant="soft",
                    ),
                    rx.button(
                        rx.color_mode_cond(
                            rx.icon("moon", size=18),
                            rx.icon("sun", size=18),
                        ),
                        cursor="pointer",
                        size=rx.breakpoints(
                            initial="2",
                            md="3",
                        ),
                        variant="soft",
                        on_click=toggle_color_mode
                    ),
                    align="center",
                    gap="0.75rem",
                ),
                align="center",
                justify_content=["space-between", "space-between", "end", "end", "end"],
                gap="0.75rem",
                width="100%"
            ),
            justify="center",
            flex_direction="column",
            height="4rem",
            padding="1rem",
            width="100%",
        ),
        # Separates navbar from the content below.
        rx.flex(
            rx.separator(),
            width="100%",
        ),
        backdrop_filter="blur(30px)",
        flex_direction="column",
        position="sticky", # Plays well with side navigation instead of fixed.
        top="0",
        width="100%",
    )

def navbar_back() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.button(
                rx.icon("arrow-left", size=18),
                cursor="pointer",
                size="3",
                variant="soft",
                on_click=rx.call_script("history.back()")
            ),
            rx.spacer(),
            rx.button(
                rx.color_mode_cond(
                    rx.icon("moon", size=18),
                    rx.icon("sun", size=18),
                ),
                cursor="pointer",
                size="3",
                variant="soft",
                on_click=toggle_color_mode
            ),
            width="100%",
        ),
        background_color="var(--gray-1)",
        flex_direction="column",
        padding="0.75rem",
        position="fixed",
        top="0",
        width="100%",
    )

def navbar_side() -> rx.Component:
    return rx.flex(
        # Side navigation bar with logo and buttons.
        rx.flex(
            # Holds logo and buttons.
            rx.flex(
                rx.flex(
                    rx.link(
                        "WP",
                        href="/home",
                        display=["none", "none", "inline", "inline", "inline"],
                        font_size="1.5rem",
                        justify_self="start",
                    ),
                    justify_content="center",
                    min_height="5rem",
                    width="100%",
                ),
                rx.flex(
                    # Home button
                    rx.flex(
                        rx.tooltip(
                            rx.button(
                                rx.icon(
                                    "home",
                                    color="var(--gray-10)",
                                ),
                                cursor="pointer",
                                size=rx.breakpoints(
                                    initial="2",
                                    md="3",
                                ),
                                variant="ghost",
                                height="100%",
                                width="100%",
                            ),
                            side="right",
                            content="Home",
                        ),
                        height="2.75rem",
                        width="2rem"
                    ),
                    # Subscriptions button
                    rx.flex(
                        rx.tooltip(
                            rx.button(
                                rx.icon(
                                    "book-open",
                                    color="var(--gray-10)",
                                ),
                                cursor="pointer",
                                size=rx.breakpoints(
                                    initial="2",
                                    md="3",
                                ),
                                variant="ghost",
                                height="100%",
                                width="100%",
                            ),
                            side="right",
                            content="Subscriptions",
                        ),
                        height="2.75rem",
                        width="2rem"
                    ),
                    # Messages button
                    rx.flex(
                        rx.tooltip(
                            rx.button(
                                rx.icon(
                                    "mail",
                                    color="var(--gray-10)",
                                ),
                                cursor="pointer",
                                size=rx.breakpoints(
                                    initial="2",
                                    md="3",
                                ),
                                variant="ghost",
                                height="100%",
                                width="100%",
                            ),
                            side="right",
                            content="Messages",
                        ),
                        height="2.75rem",
                        width="2rem"
                    ),
                    # Search button
                    rx.flex(
                        rx.tooltip(
                            rx.button(
                                rx.icon(
                                    "search",
                                    color="var(--gray-10)",
                                ),
                                cursor="pointer",
                                size=rx.breakpoints(
                                    initial="2",
                                    md="3",
                                ),
                                variant="ghost",
                                height="100%",
                                width="100%",
                            ),
                            side="right",
                            content="Search",
                        ),
                        height="2.75rem",
                        width="2rem"
                    ),
                    flex_direction="column",
                    gap="1.25rem",
                    height="100%",
                    justify_content="center",
                ),
                flex_direction="column",
                height="100%",
            ),
            height="100%",
            padding="1rem 1.25rem 1rem 1.25rem",
        ),
        rx.separator(orientation="vertical"),
        background_color="var(--gray-1)",
        height="100vh",
        position="sticky",
    )