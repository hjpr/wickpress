import reflex as rx

from reflex.style import toggle_color_mode

from .menus import mobile_menu, account_menu
from .modals import search_modal_for_navbar
from ..states.auth import AuthState
from ..states.base import BaseState
from ..states.page import PageState


def navbar() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.link(
                    "WP",
                    size="7",
                    href="/home",
                ),
                height="4.5rem",
                width="4.5rem",
                align="center",
                justify="center",
                border_right=rx.cond(
                    PageState.current_page == "/about",
                    "none",
                    "1px solid var(--gray-3)",
                ),
                border_bottom=rx.cond(
                    PageState.current_page == "/about",
                    "1px solid var(--gray-3)",
                    "none"
                ),
                display=rx.breakpoints(
                    xs="none",
                    sm="flex",
                    md="flex",
                    lg="flex",
                    xl="flex"
                )
            ),

            mobile_menu(),

            flex_shrink="0",
            align="center",
            justify="center",
            height="4.5rem",
            width="4.5rem",

        ),

        # Main navigation bar with logo and buttons.
        rx.flex(
            # Holds logo and buttons.
            rx.flex(
                rx.flex(
                    # Current page title.
                    rx.cond(
                        PageState.current_page != "/about",
                        rx.heading(PageState.current_page_formatted)
                    ),
                    padding="0 1rem",
                    user_select="none",
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

                    # Show sign in button when user is not logged in.
                    rx.cond(
                        BaseState.user_is_authenticated,
                        account_menu(
                            rx.button(
                                rx.icon("user", size=18),
                                cursor="pointer",
                                variant="soft"
                            )
                        ),
                        rx.button(
                            rx.text(
                                "Sign in",
                                on_click=rx.redirect("/sign-in")
                            ),
                            cursor="pointer",
                            variant="soft",
                        )
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
                on_click=rx.call_script(
                    "history.back()",
                    callback=PageState.default_script_callback
                )
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

            # Holds buttons
            rx.flex(
                # Home button
                rx.flex(
                    rx.tooltip(
                        rx.flex(
                            rx.icon(
                                "home",
                                color="var(--gray-10)",
                            ),
                            align="center",
                            justify="center",
                            cursor="pointer",
                            height="100%",
                            width="100%",
                            on_click=rx.redirect("/home")
                        ),
                        side="right",
                        content="Home",
                    ),
                    background_color=rx.cond(
                        PageState.current_page == "/home",
                        "var(--gray-3)",
                        "none"
                    ),
                    border_radius="0.5rem",
                    height="3.5rem",
                    width="3.5rem"
                ),
                # Library button
                rx.cond(
                    AuthState.user_is_authenticated,
                    rx.flex(
                        rx.tooltip(
                            rx.flex(
                                rx.icon(
                                    "library-big",
                                    color="var(--gray-10)",
                                ),
                                cursor="pointer",
                                align="center",
                                justify="center",
                                height="100%",
                                width="100%",
                                on_click=rx.redirect("/library")
                            ),
                            side="right",
                            content="Library",
                        ),
                        background_color=rx.cond(
                            PageState.current_page == "/library",
                            "var(--gray-3)",
                            "none"
                        ),
                        border_radius="0.5rem",
                        height="3.5rem",
                        width="3.5rem",
                        _hover={
                            "backgroundColor": "var(--gray-3)"
                        },
                    )
                ),
                # Discover button
                rx.flex(
                    rx.tooltip(
                        rx.flex(
                            rx.icon(
                                "telescope",
                                color="var(--gray-10)",
                            ),
                            align="center",
                            justify="center",
                            cursor="pointer",
                            height="100%",
                            width="100%",
                            on_click=rx.redirect("/discover")
                        ),
                        side="right",
                        content="Discover",
                    ),
                    background_color=rx.cond(
                        PageState.current_page == "/discover",
                        "var(--gray-3)",
                        "none"
                    ),
                    border_radius="0.5rem",
                    height="3.5rem",
                    width="3.5rem",
                    _hover={
                        "backgroundColor": "var(--gray-3)"
                    },
                ),
                # Messages button
                rx.cond(
                    AuthState.user_is_authenticated,
                    rx.flex(
                        rx.tooltip(
                            rx.flex(
                                rx.icon(
                                    "mail",
                                    color="var(--gray-10)",
                                ),
                                align="center",
                                justify="center",
                                cursor="pointer",
                                height="100%",
                                width="100%",
                                on_click=rx.redirect("/messages")
                            ),
                            side="right",
                            content="Messages",
                        ),
                        background_color=rx.cond(
                            PageState.current_page == "/messages",
                            "var(--gray-3)",
                            "none"
                        ),
                        border_radius="0.5rem",
                        height="3.5rem",
                        width="3.5rem",
                        _hover={
                            "backgroundColor": "var(--gray-3)"
                        },
                    )
                ),
                # Search button
                rx.flex(
                    rx.tooltip(
                        rx.flex(
                            rx.icon(
                                "search",
                                color="var(--gray-10)",
                            ),
                            align="center",
                            justify="center",
                            cursor="pointer",
                            height="100%",
                            width="100%",
                            on_click=PageState.setvar("search_modal_open", ~PageState.search_modal_open)
                        ),
                        side="right",
                        content="Search",
                    ),
                    border_radius="0.5rem",
                    height="3.5rem",
                    width="3.5rem",
                    _hover={
                        "backgroundColor": "var(--gray-3)"
                    },
                ),
                flex_direction="column",
                flex_shrink="0",
                gap="1rem",
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