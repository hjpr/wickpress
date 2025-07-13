import reflex as rx

from ..components import navbar

@rx.page(
    route="/about",
    title="Wick Press"
)
def about() -> rx.Component:
    return rx.flex(
        navbar(),
        rx.flex(
            hero(),
            rx.separator(),
            s1(),
            rx.separator(),
            s2(),
            rx.separator(),
            s3(),
            rx.separator(),
            flex_direction="column",
            width="100%",
        ),
        background_color="var(--gray-1)",
        flex_direction="column",
        flex_grow="1",
        min_height="100vh",
    )

def hero() -> rx.Component:
    return rx.flex(
        rx.color_mode_cond(
            rx.text(
                "Short stories and tall tales.",
                class_name="text-4xl text-center"
            ),
            rx.text(
                "Spooky stories and tall tales.",
                class_name="text-4xl text-center"
            ), 
        ),
        align="center",
        background_color="var(--gray-1)",
        justify="center",
        height="28rem",
        width="100%",
    )

def s1() -> rx.Component:
    return rx.flex(
        rx.text(
            "Section 1",
        ),
        align="center",
        background_color="var(--gray-1)",
        justify="center",
        height="24rem",
        width="100%",
    )

def s2() -> rx.Component:
    return rx.flex(
        rx.text(
            "Section 2",
        ),
        align="center",
        background_color="var(--gray-1)",
        justify="center",
        height="24rem",
        width="100%",
    )

def s3() -> rx.Component:
    return rx.flex(
        rx.text(
            "Section 3",
        ),
        align="center",
        background_color="var(--gray-1)",
        justify="center",
        height="24rem",
        width="100%",
    )