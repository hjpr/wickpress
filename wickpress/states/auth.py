
import reflex as rx

from loguru import logger
from httpx import HTTPStatusError
from rich.console import Console
from typing import Callable, Iterable

from .base import BaseState
from .user import UserState

console = Console()

class AuthState(BaseState):
    
    def sign_in(self, form_data: dict) -> Iterable[Callable]:
        try:
            user = {}
            email = form_data.get("email")
            password = form_data.get("password")
            user_data = self.sign_in_with_password(
                email=email,
                password=password
            )

            # Pull supabase user object to state
            user["supabase"] = user_data.get("user", {})

            # Pull website profile to state, if first login, create entry
            user["wickpress"] = (
                self.query()
                .table("profiles")
                .select("*")
                .eq("id", user["supabase"]["id"])
                .execute()
            )

            if not user["wickpress"]:
                self.query().table("profiles").insert({"id": user["supabase"]["id"]}).execute()
            else:
                user["wickpress"] = user["wickpress"][0]

            yield UserState.setvar("user", user)
            yield rx.redirect("/home")

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