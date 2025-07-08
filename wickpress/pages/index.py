import reflex as rx

from ..components import navbar

@rx.page(
    route="/",
    title="Wick Press"
)
def index() -> rx.Component:
    return rx.flex(
        navbar(),
        class_name="flex bg-white w-full h-screen"
    )