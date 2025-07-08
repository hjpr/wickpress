
import reflex as rx

def tw_flex(
        *children,
        bg_color: str = "",
        bg_color_dark: str = "",
        border: bool = False,
        border_radius: str = "",
        border_color: str = "",
        **props
    ) -> rx.Component:
    tailwind_classes = (
        (f"bg-{bg_color} " if bg_color else "") +\
        (f"dark:bg-{bg_color_dark} " if bg_color_dark else "") +\
        ("border " if border else "") +\
        (f"rounded-{border_radius} " if border_radius else "") +\
        (f"border-{border_color} " if border_color else "")
    )
    return rx.button(
        *children,
        **props,
        class_name=tailwind_classes.strip(),
    )