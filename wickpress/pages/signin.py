
import reflex as rx

from ..states.user import UserState
from ..components.navbars import navbar_back

@rx.page(
    route="/sign-in"
)
def signin() -> rx.Component:
    return rx.flex(
        navbar_back(),
            rx.flex(
                rx.flex(
                    rx.heading("Sign in to Wick Press", size="7"),
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
                    rx.button(
                        "Continue",
                        cursor="pointer",
                        type_="submit",
                        size="4",
                        class_name="inset-shadow-sm"
                    ),
                    display="flex",
                    gap="1.5rem",
                    flex_direction="column",
                    justify="center",
                    width="100%",
                    on_submit=UserState.sign_in
                ),
                rx.flex(
                    rx.text(
                        "Are you new here? ",
                        rx.link(
                            "Sign up",
                            href="/sign-up",
                            class_name="text-rose-500 hover:text-rose-600"
                        )
                    ),
                    justify="center",
                    padding="1.5rem 0 1.5rem 0",
                    width="100%",
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