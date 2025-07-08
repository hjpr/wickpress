
import reflex as rx

def tw_button(
        *children,
        text_size: str = "sm",
        text_color: str = "white",
        text_color_dark: str = "black",
        bg_color: str = "red-500",
        bg_color_dark: str = "gray-800",
        bg_color_hover: str = "blue-600",
        border: bool = True,
        border_radius: str = "md",
        border_color: str = "gray-600",
        border_color_dark: str = "gray-700",
        
        cursor: str = "pointer",
        **props
    ) -> rx.Component:
    tailwind_classes = (
        (f"text-{text_size} " if text_size else "") +\
        (f"text-{text_color} " if text_color else "") +\
        (f"dark:text-{text_color_dark} " if text_color_dark else "") +\
        (f"bg-{bg_color} " if bg_color else "") +\
        (f"dark:bg-{bg_color_dark} " if bg_color_dark else "") +\
        (f"hover:bg-{bg_color_hover} " if bg_color_hover else "") +\
        ("border " if border else "") +\
        (f"rounded-{border_radius} " if border_radius else "") +\
        (f"border-{border_color} " if border_color else "") +\
        (f"dark:border-{border_color_dark} " if border_color_dark else "") +\
        (f"cursor-{cursor} " if cursor else "")
    )
    return rx.button(
        *children,
        **props,
        class_name=tailwind_classes.strip(),
    )

def tw_button_ghost(*children, **props) -> rx.Component:
    """A Tailwind-styled ghost button component."""
    return rx.button(
        *children,
        **props,
        class_name="",
    )