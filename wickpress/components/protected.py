
import functools
import reflex as rx

from ..states.auth import AuthState

def login_protected(page) -> rx.Component:
    @functools.wraps(page)
    def _wrapper() -> rx.Component:
        return rx.cond(AuthState.user_is_authenticated, page(), rx.box())

    return _wrapper