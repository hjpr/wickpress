
import reflex as rx

from ..states.auth import AuthState

def mobile_menu() -> rx.Component:
    return rx.drawer.root(
        rx.drawer.trigger(
            rx.flex(
                rx.icon(
                    "menu",
                    size=24,
                    cursor="pointer",
                ),
                align="center",
                justify="center",
                width="4.5rem",
                height="4.5rem",
                border_bottom="1px solid var(--gray-3)",
                display=rx.breakpoints(
                    xs="flex",
                    sm="none",
                    md="none",
                    lg="none",
                    xl="none"
                ),
            )
        ),
        rx.drawer.portal(
            rx.drawer.content(
                rx.flex(
                    rx.drawer.close(rx.box(rx.button("Close"))),
                    flex_direction="column",
                ),
                background_color="var(--gray-1)",
                height="100%",
                padding="2em",
                top="4.5rem",
                width="100%"
            )
        ),
        direction="left",
    )

def account_menu(button: rx.Component) -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            button
        ),
        rx.menu.content(
            rx.menu.item(
                "Logout",
                on_click=[
                    AuthState.log_out,
                    rx.redirect("/")
                ]
            )
        )
    )
