
import reflex as rx

def tw_flex(
        *children,
        bg_color: str = "neutral-50",
        bg_color_dark: str = "neutral-900",
        border: bool = False,
        border_radius: str = "",
        border_color: str = "",
        **props
    ) -> rx.Component:
    tailwind_classes = (
        ("flex ") +\
        (f"bg-{bg_color} " if bg_color else "") +\
        (f"dark:bg-{bg_color_dark} " if bg_color_dark else "") +\
        ("border " if border else "") +\
        (f"rounded-{border_radius} " if border_radius else "") +\
        (f"border-{border_color} " if border_color else "")
    )
    class_name = props.pop("class_name", None)  # Remove class_name if it exists to avoid conflicts
    return rx.flex(
        *children,
        **props,
        class_name=(
            tailwind_classes.strip() +
            (f" {class_name}" if class_name else "")
        )
    )