
import reflex as rx

from rxconfig import config
from .pages import *
from .states import *

style = {
    rx.button: {
        "border_radius": "0.75rem"
    },
    rx.input: {
        "border_radius": "0.75rem"
    },
    rx.separator: {
        "background_color": "var(--gray-4)",
    },
    rx.text_area: {
        "border_radius": "0.75rem"
    },
    rx.text_field: {
        "border_radius": "0.75rem"
    }
}

app = rx.App(
    style=style,
    stylesheets=["/styles.css"],
    theme=rx.theme(
        accent_color="ruby",
        radius="large"
    ),
    toaster=rx.toast.provider(
        close_button=True,
        position="top-center",
        toast_options=rx.toast.options(
            duration=3000
        )
    )
)