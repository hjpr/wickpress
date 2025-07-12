
import reflex as rx

from .base import BaseState
from loguru import logger
from httpx import HTTPStatusError
from rich.console import Console
from typing import Callable, Iterable

console = Console()

class AuthState(BaseState):
    
    def sign_in(self, form_data: dict) -> Iterable[Callable]:
        try:
            self.sign_in_with_password(
                email=form_data.get("email"),
                password=form_data.get("password")
            )
            # If successful.
        except HTTPStatusError as e:
            console.print_exception()
            yield rx.toast.error(
                e.response.json()["msg"],
                position="bottom-center"
            )
            yield AuthState.setvar("is_loading", False)
        except Exception as e:
            console.print_exception()
            yield rx.toast.error(
                str(e),
                position="bottom-center"
            )
            yield AuthState.setvar("is_loading", False)

    def create_account(self, form_data: dict) -> Iterable[Callable]:
        yield rx.toast.info(
            "Creating account...",
            position="bottom-center"
        )
        yield AuthState.setvar("is_loading", False)