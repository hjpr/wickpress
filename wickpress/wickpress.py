
import reflex as rx

from rxconfig import config
from .pages import *
from .states import *

style = {
    "font_family": "monospace",
}

app = rx.App(
    style=style,
    theme=rx.theme(
        accent_color="ruby",
        radius="large"
    )
)