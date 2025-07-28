
import reflex as rx

from functools import wraps
from rich.console import Console
from suplex import Suplex

console = Console()

class BaseState(Suplex):

    def check_router_data(self) -> None:
        """
        This method is a placeholder to demonstrate how to access router data.
        It can be expanded to include actual logic for checking router data.
        """
        console.print(f"{self.router.url.path}")
        # Here you can add logic to handle the router data as needed.