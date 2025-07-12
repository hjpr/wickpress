
import reflex as rx

from rich.console import Console
from suplex import Suplex

console = Console()

class BaseState(Suplex):

    @rx.var
    def current_page(self) -> str:
        return self.router.url.path

    def check_router_data(self):
        """
        This method is a placeholder to demonstrate how to access router data.
        It can be expanded to include actual logic for checking router data.
        """
        console.print(f"{self.router.url.path}")
        # Here you can add logic to handle the router data as needed.