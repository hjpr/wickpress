import reflex as rx

from reflex.style import toggle_color_mode

def navbar() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.text(
                    "Wick Press",
                    display=["none", "none", "inline", "inline", "inline"],
                    font_size="1.5rem"
                ),
                rx.spacer(),
                rx.flex(
                    rx.button(
                        rx.text(
                            "Start publishing",
                        ),
                        cursor="pointer",
                        size=rx.breakpoints(
                            initial="2",
                            md="3",
                        ),
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
                width="100%"
            ),
            background_color="var(--gray-1)",
            flex_direction="column",
            padding="0.75rem",
            width="100%",
        ),
        rx.flex(
            rx.separator(),
            width="100%",
        ),
        flex_direction="column",
        position="fixed",
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