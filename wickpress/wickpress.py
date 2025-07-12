
import reflex as rx

from rxconfig import config
from .pages import *
from .states import *

style = {
    "font_family": "monospace",
    rx.separator: {
        "background_color": "var(--gray-4)",
    }
}

app = rx.App(
    style=style,
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