
import reflex as rx
    
def slim_message(message: dict[str, str]) -> rx.Component:
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
        # Content container
        rx.flex(
            rx.flex(
                rx.text(
                    message["content"]["subject"]
                ),
                height="1rem"
            ),
            rx.flex(
                rx.icon("star", size=18),
                rx.icon("trash", size=18),
                justify="end",
                gap="1rem",
                height="1rem",
                width="100%"
            ),
            flex_direction="column",
            gap="1rem",
            width="100%"
        ),
        display="flex",
        flex_direction="row",
        justify="center",
        gap="1rem",
        padding="1rem"
    )

def expanded_message(message: dict[str, str]) -> rx.Component:
    return rx.flex()
