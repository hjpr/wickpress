
import reflex as rx

from ..states.auth import AuthState
from ..components.nav_bars import navbar_back

@rx.page(
    route="/forgot-password",
    title="Forgot Password - Wick Press"
)
def forgot_password() -> rx.Component:
    return rx.flex(
        navbar_back(),

        # Contains main content
        rx.flex(

            # Contains the main content of the sign-in page.
            rx.flex(
                rx.flex(
                    rx.heading(
                        "W",
                        size="9",
                    ),
                    justify="center",
                    padding="0 0 2rem 0",
                    width="100%",
                ),
                rx.flex(
                    rx.heading(
                        "Forgot your password?",
                        size="6",
                        text_align="center"
                    ),
                    justify="center"
                ),
                rx.flex(
                    rx.text(
                        "We'll send a one-time use link that will log you in. You'll be able to change your password within your account settings.",
                        size="2",
                        text_align="center"
                    ),
                    padding="1.5rem 0 1.5rem 0",
                ),
                rx.form(
                    rx.input(
                        height="2.75rem",
                        name="email",
                        placeholder="Email",
                        size="3",
                        type="email",
                        required=True
                    ),
                    rx.button(
                        "Send link",
                        cursor="pointer",
                        loading=AuthState.is_loading,
                        type_="submit",
                        size="4",
                        class_name="inset-shadow-sm"
                    ),
                    display="flex",
                    flex_direction="column",
                    gap="1.5rem",
                    justify="center",
                    width="100%",
                    on_submit=[
                        AuthState.setvar("is_loading", True),
                        AuthState.forgot_password
                    ]
                ),
                flex_direction="column",
                flex_grow="1",
                max_width="26rem",
                padding="5rem 0 0 0",
            ),
            bg="var(--gray-1)",
            flex_direction="row",
            justify="center",
            flex_grow="1",
        ),
        flex_direction="column",
        scroll_padding_top="4.5rem",
        height="100vh",
        width="100%",
    )