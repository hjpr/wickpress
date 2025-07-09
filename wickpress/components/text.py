
import reflex as rx

def tw_text(
        *children,
        text_size: str = "base",
        text_color: str = "black",
        text_color_dark: str = "white",
        font_type: str = "mono",
        font_weight: str = "normal",
        font_style: str = "normal",
        **props
    ) -> rx.Component:
    tailwind_classes = (
        (f"text-{text_size} " if text_size else "") +
        (f"text-{text_color} " if text_color else "") +
        (f"dark:text-{text_color_dark} " if text_color_dark else "") +
        (f"font-{font_type} " if font_type else "") +
        (f"font-{font_weight} " if font_weight else "") +
        (f"italic " if font_style == "italic" else "")
    )
    class_name = props.pop("class_name", "")
    return rx.text(
        *children,
        **props,
        class_name=(
            tailwind_classes.strip() +
            (f" {class_name}" if class_name else "")
        )
    )