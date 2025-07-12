
import reflex as rx

from ..states.auth import AuthState
from ..components.navbars import navbar_back

@rx.page(
    route="/sign-up",
    title="Sign Up - Wick Press"
)
def signup() -> rx.Component:
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
                    rx.heading("Create your account", size="7"),
                    justify="center",
                    padding="0 0 2rem 0",
                ),
                rx.form(
                    rx.input(
                        height="3rem",
                        name="email",
                        placeholder="Email",
                        size="3",
                        type="email",
                        required=True
                    ),
                    rx.input(
                        height="3rem",
                        name="password",
                        placeholder="Password",
                        size="3",
                        type="password",
                        required=True
                    ),
                    rx.input(
                        height="3rem",
                        name="reenter_password",
                        placeholder="Re-Enter Password",
                        size="3",
                        type="password",
                        required=True
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
                        AuthState.create_account
                    ]
                ),
                flex_direction="column",
                width="26rem"
            ),
        align="center",
        background_color="var(--gray-1)",
        flex_direction="column",
        height="100vh",
        padding="4rem 0 0 0",
        width="100%",
    )