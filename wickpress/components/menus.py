
import reflex as rx

def mobile_menu() -> rx.Component:
    return rx.drawer.root(
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
                    flex_direction="column",
                ),
                background_color="var(--gray-1)",
                height="100%",
                padding="2em",
                top="4.25rem",
                width="100%",
            )
        ),
        direction="left",
    )