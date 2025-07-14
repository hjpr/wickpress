
import reflex as rx

from ..states.auth import AuthState
from ..components.navbars import navbar_back

@rx.page(
    route="/sign-in",
    title="Sign In - Wick Press"
)
def signin() -> rx.Component:
    return rx.flex(
        navbar_back(),
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
                    "Sign in to Wick Press",
                    size="6",
                    text_align="center"
                ),
                justify="center",
                padding="0 0 2rem 0",
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
                rx.input(
                    height="2.75rem",
                    name="password",
                    placeholder="Password",
                    size="3",
                    type="password",
                    required=True
                ),
                rx.flex(
                    rx.link(
                        "Forgot Password?",
                        href="/forgot-password",
                        size="2",
                    ),
                    justify="center",
                    width="100%"
                ),
                rx.button(
                    "Continue",
                    cursor="pointer",
                    loading=AuthState.is_loading,
                    type_="submit",
                    size="4",
                    class_name="inset-shadow-sm"
                ),
                display="flex",
                gap="1.5rem",
                flex_direction="column",
                justify="center",
                width="100%",
                on_submit=[
                    AuthState.setvar("is_loading", True),
                    AuthState.sign_in
                ]
            ),
            rx.flex(
                rx.text(
                    "Are you new here? ",
                    rx.link(
                        "Sign up",
                        href="/sign-up",
                    ),
                    size="2"
                ),
                align="center",
                flex_direction="column",
                gap="1rem",
                padding="1.5rem 0 1.5rem 0",
                width="100%",
            ),
            flex_direction="column",
            max_width="26rem",
            width="100%",
        ),
        align="center",
        background_color="var(--gray-1)",
        flex_direction="column",
        min_height="100vh",
        padding="4rem 2rem 2rem 2rem",
        width="100%",
    )