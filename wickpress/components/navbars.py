import reflex as rx

from ..components.menus import mobile_menu
from ..components.modals import search_modal_for_navbar
from reflex.style import toggle_color_mode
from ..states.page import PageState


def navbar() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.link(
                "WP",
                size="7",
                href="/home",
                display=["none", "none", "inline", "inline", "inline"],
            ),
            border_right="1px solid var(--gray-3)",
            flex_shrink="0",
            align="center",
            justify="center",
            height="4.5rem",
            width="4.5rem",
            display=rx.breakpoints(
                xs="none",
                sm="flex",
                md="flex",
                lg="flex",
                xl="flex"
            )
        ),

        # Main navigation bar with logo and buttons.
        rx.flex(
            # Holds logo and buttons.
            rx.flex(
                rx.flex(
                    mobile_menu(),
                    padding="0 0 0 1rem",
                ),
                rx.flex(
                    # Current page title.
                    rx.cond(
                        PageState.current_page != "/about",
                        rx.heading(PageState.current_page_formatted)
                    ),
                    padding="0 1rem"
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

                # Holds the buttons for the navbar.
                rx.flex(
                    # Show publish button only when at the about page.
                    rx.cond(
                        PageState.current_page == "/about",
                        rx.button(
                            rx.text(
                                "Start writing",
                            ),
                            cursor="pointer",
                        )
                    ),
                    rx.button(
                        rx.text(
                            "Sign in",
                            on_click=rx.redirect("/sign-in")
                        ),
                        cursor="pointer",
                        variant="soft",
                    ),
                    rx.button(
                        rx.color_mode_cond(
                            rx.icon("moon", size=18),
                            rx.icon("sun", size=18),
                        ),
                        cursor="pointer",
                        variant="soft",
                        on_click=toggle_color_mode
                    ),
                    flex_shrink="0",
                    gap="0.75rem",
                    padding="0 1rem 0 0"
                ),
                align="center",
                justify="end",
                gap="0.75rem",
                width="100%"
            ),
            border_bottom="1px solid var(--gray-3)",
            justify="center",
            flex_direction="column",
            width="100%"
        ),
        bg="var(--gray-1)",
        height="4.5rem",
        position="fixed",
        width="100%",
        z_index="100"
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
            flex_grow="1",
            justify_content="space-between",
        ),
        align="center",
        bg="var(--gray-1)",
        height="4.5rem",
        position="fixed",
        padding="0 1rem",
        width="100%",
        z_index="100"
    )

def navbar_side() -> rx.Component:
    return rx.flex(
        # Holds logo and buttons.
        rx.flex(
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
                    height="2.5rem",
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
                    height="2.5rem",
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
                    height="2.5rem",
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
                    height="2.5rem",
                    width="2rem"
                ),
                flex_direction="column",
                flex_shrink="0",
                gap="1.25rem",
                align="center",
                justify="center"
            ),
            align="center",
            justify_content="space-around",
            flex_direction="column",
            width="100%",
            overflow="hidden",
        ),
        background_color="var(--gray-1)",
        border_right="1px solid var(--gray-3)",
        height="100%",
        width="4.5rem",
        padding="4.5rem 0 0 0",
        position="fixed",
        display=rx.breakpoints(
            xs="none",
            sm="flex",
            md="flex",
            lg="flex",
            xl="flex",
        ),
    )