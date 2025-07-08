import reflex as rx

from .buttons import tw_button, tw_button_ghost

def navbar() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text("Wick", class_name="text-black text-2xl font-bold"),
            rx.spacer(),
            tw_button(
                "Log In",
                ),
            class_name="flex border border-gray-600 w-full"
        ),
        class_name="flex bg-white dark:bg-black px-8 py-4 w-full h-16"
    )