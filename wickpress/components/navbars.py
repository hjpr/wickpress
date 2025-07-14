import reflex as rx

from ..components.menus import mobile_menu
from ..components.modals import search_modal_for_navbar
from reflex.style import toggle_color_mode
from ..states.page import PageState


def navbar() -> rx.Component:
    return rx.flex(
        # Main navigation bar with logo and buttons.
        rx.flex(
            # Holds logo and buttons.
            rx.flex(
                rx.flex(
                    mobile_menu(),
                ),
                rx.flex(
                    # Current page title.
                    rx.cond(
                        PageState.current_page != "/about",
                        rx.heading(PageState.current_page_formatted)
                    ),
                ),

                # Search input field only on the home page.
                rx.cond(
                    PageState.current_page != "/about",
                    rx.flex(
                        rx.form(
                            rx.input(
                                search_modal_for_navbar(),
                                name="search_input",
                                placeholder="Search...",
                                display=["none", "none", "flex", "flex", "flex"],
                                max_width="24rem",
                                min_width="18rem",
                                size=rx.breakpoints(
                                    initial="2",
                                    md="3",
                                ),
                                width="100%",
                            ),
                            display="flex",
                            width="auto",
                            reset_on_submit=True,
                            on_submit=[
                                PageState.setvar("is_loading", True),
                                PageState.submit_search_from_navbar,
                            ]
                        ),
                        justify="end",
                        width="100%"
                    )
                ),

                rx.flex(
                    # Show publish button only when at the about page.
                    rx.cond(
                        PageState.current_page == "/about",
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
                    flex_shrink="0",
                    gap="0.75rem",
                ),
                align="center",
                justify="end",
                gap="0.75rem",
                width="100%"
            ),
            justify="center",
            flex_direction="column",
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
                                on_click=rx.redirect("/home")
                            ),
                            side="right",
                            content="Home",
                        ),
                        height="2.75rem",
                        width="2rem"
                    ),
                    # Library button
                    rx.flex(
                        rx.tooltip(
                            rx.button(
                                rx.icon(
                                    "library-big",
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
                                on_click=rx.redirect("/library")
                            ),
                            side="right",
                            content="Library",
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
                                on_click=rx.redirect("/messages")
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
                                on_click=PageState.setvar("search_modal_open", ~PageState.search_modal_open)
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