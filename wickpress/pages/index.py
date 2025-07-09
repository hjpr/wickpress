import reflex as rx

from ..components import navbar

@rx.page(
    route="/",
    title="Wick Press"
)
def index() -> rx.Component:
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
            padding="4rem 0 0 0",
            width="100%",
        ),
        class_name="flex-col w-full h-screen"
    )

def hero() -> rx.Component:
    return rx.flex(
        rx.text(
            "Short stories and tall tales.",
            class_name="text-4xl text-center"
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