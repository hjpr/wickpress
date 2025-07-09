
import reflex as rx

def tw_button(
        *children,
        text_size: str = "sm",
        text_color: str = "black",
        text_color_dark: str = "white",
        bg_color: str = "white",
        bg_color_dark: str = "neutral-800",
        bg_color_hover: str = "",
        bg_color_hover_dark: str = "neutral-700",
        border: bool = True,
        border_radius: str = "md",
        border_color: str = "black",
        border_color_dark: str = "white",
        padding: str = "p-5",
        cursor: str = "pointer",
        **props
    ) -> rx.Component:
    tailwind_classes = (
        (f"text-{text_size} " if text_size else "") +
        (f"text-{text_color} " if text_color else "") +
        (f"dark:text-{text_color_dark} " if text_color_dark else "") +
        (f"bg-{bg_color} " if bg_color else "") +
        (f"dark:bg-{bg_color_dark} " if bg_color_dark else "") +
        (f"hover:bg-{bg_color_hover} " if bg_color_hover else "") +
        (f"dark:hover:bg-{bg_color_hover_dark} " if bg_color_hover_dark else "") +
        ("border " if border else "") +
        (f"rounded-{border_radius} " if border_radius else "") +
        (f"border-{border_color} " if border_color else "") +
        (f"dark:border-{border_color_dark} " if border_color_dark else "") +
        (f"{padding} " if padding else "") +
        (f"cursor-{cursor} " if cursor else "")
    )
    class_name = props.pop("class_name", None)  # Remove class_name if it exists to avoid conflicts
    return rx.button(
        *children,
        **props,
        class_name=(
            tailwind_classes.strip() +
            (f" {class_name}" if class_name else "")
        )
    )

def tw_button_solid(
        *children,
        text_size: str = "sm",
        text_color: str = "white",
        text_color_dark: str = "white",
        bg_color: str = "rose-500",
        bg_color_dark: str = "red-400",
        bg_color_hover: str = "rose-400",
        bg_color_hover_dark: str = "rose-600",
        border: bool = False,
        border_radius: str = "lg",
        border_color: str = "",
        border_color_dark: str = "",
        inset_shadow: bool = True,
        padding: str = "p-5",
        cursor: str = "pointer",
        **props
    ) -> rx.Component:
    tailwind_classes = (
        (f"text-{text_size} " if text_size else "") +
        (f"text-{text_color} " if text_color else "") +
        (f"dark:text-{text_color_dark} " if text_color_dark else "") +
        ("font-bold ") +
        (f"bg-{bg_color} " if bg_color else "") +
        (f"dark:bg-{bg_color_dark} " if bg_color_dark else "") +
        (f"hover:bg-{bg_color_hover} " if bg_color_hover else "") +
        (f"dark:hover:bg-{bg_color_hover_dark} " if bg_color_hover_dark else "") +
        ("border " if border else "") +
        (f"rounded-{border_radius} " if border_radius else "") +
        (f"border-{border_color} " if border_color else "") +
        (f"dark:border-{border_color_dark} " if border_color_dark else "") +
        ("shadow-inner " if inset_shadow else "") +
        (f"{padding} " if padding else "") +
        (f"cursor-{cursor} " if cursor else "")
    )
    class_name = props.pop("class_name", None)  # Remove class_name if it exists to avoid conflicts
    return rx.button(
        *children,
        **props,
        class_name=(
            tailwind_classes.strip() +
            (f" {class_name}" if class_name else "")
        )
    )

def tw_button_ghost(
        *children,
        text_size: str = "sm",
        text_color: str = "black",
        text_color_dark: str = "white",
        bg_color: str = "transparent",
        bg_color_dark: str = "transparent",
        bg_color_hover: str = "neutral-200",
        bg_color_hover_dark: str = "neutral-800",
        border: bool = False,
        border_radius: str = "lg",
        border_color: str = "",
        border_color_dark: str = "",
        padding: str = "p-5",
        cursor: str = "pointer",
        **props
    ) -> rx.Component:
    tailwind_classes = (
        (f"text-{text_size} " if text_size else "") +
        (f"text-{text_color} " if text_color else "") +
        (f"dark:text-{text_color_dark} " if text_color_dark else "") +
        (f"bg-{bg_color} " if bg_color else "") +
        (f"dark:bg-{bg_color_dark} " if bg_color_dark else "") +
        (f"hover:bg-{bg_color_hover} " if bg_color_hover else "") +
        (f"dark:hover:bg-{bg_color_hover_dark} " if bg_color_hover_dark else "") +
        ("border " if border else "") +
        (f"rounded-{border_radius} " if border_radius else "") +
        (f"border-{border_color} " if border_color else "") +
        (f"dark:border-{border_color_dark} " if border_color_dark else "") +
        (f"{padding} " if padding else "") +
        (f"cursor-{cursor} " if cursor else "")
    )
    class_name = props.pop("class_name", None)  # Remove class_name if it exists to avoid conflicts
    return rx.button(
        *children,
        **props,
        class_name=(
            tailwind_classes.strip() +
            (f" {class_name}" if class_name else "")
        )
    )