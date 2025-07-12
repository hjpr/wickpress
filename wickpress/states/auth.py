
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
            email = form_data.get("email")
            password = form_data.get("password")
            console.print(f"Signing in {email} via password...")
            self.sign_in_with_password(
                email=email,
                password=password,
            )
            console.print(f"Successfully signed in {email} with password.")

        except HTTPStatusError as e:
            console.print_exception()
            yield rx.toast.error(e.response.json()["msg"])
        except Exception as e:
            console.print_exception()
            yield rx.toast.error(str(e))
        finally:
            yield AuthState.setvar("is_loading", False)

    def create_account(self, form_data: dict) -> Iterable[Callable]:
        email = form_data.get("email")
        password = form_data.get("password")
        reenter_password = form_data.get("reenter_password")

        if password != reenter_password:
            yield rx.toast.error("Passwords do not match.")
            yield AuthState.setvar("is_loading", False)
            return
        
        if len(password) < 8:
            yield rx.toast.error("Password must be at least 8 characters long.")
            yield AuthState.setvar("is_loading", False)
            return
        
        try:
            console.print(f"Creating account for {email}")
            self.sign_up(
                email=email,
                password=password,
            )
            console.print(f"Successfully created account for {email}")
            yield rx.toast.success(
                "Account created successfully. Please check your email to verify your account."
            )
        except HTTPStatusError as e:
            console.print_exception()
            yield rx.toast.error(e.response.json()["msg"])
        except Exception as e:
            console.print_exception()
            yield rx.toast.error(str(e))
        finally:
            yield AuthState.setvar("is_loading", False)

    def forgot_password(self, form_data: dict) -> Iterable[Callable]:
        email = form_data.get("email")
        if not email:
            yield rx.toast.error("Email is required.")
            yield AuthState.setvar("is_loading", False)
            return
        
        try:
            console.print(f"Sending password reset link to {email}")
            self.reset_password_email(email=email)
            yield rx.toast.success("Password reset link sent to your email.")
        except Exception as e:
            console.print_exception()
            yield rx.toast.error(str(e))
        finally:
            yield AuthState.setvar("is_loading", False)