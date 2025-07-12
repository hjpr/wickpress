import reflex as rx

@rx.page(
    route="/",
    on_load=rx.redirect("/about", replace=True)
)
def index() -> rx.Component:
    return rx.flex()