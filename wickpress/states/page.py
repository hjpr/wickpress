
import reflex as rx

from .base import BaseState
from rich.console import Console
from typing import Callable, Iterable

console = Console()

class PageState(BaseState):
    """
    PageState extends BaseState to manage page-specific state and behavior.
    It can include additional methods or properties specific to page management.
    """

    search_modal_open: bool = False
    search_input: str = ""
    search_results: list = []
    trending_topics: list[dict[str, str]] = [
        {"name": "A crazy trending topic"},
        {"name": "Another interesting topic"},
        {"name": "Latest news in tech"},
    ]

    @rx.var
    def current_page(self) -> str:
        return self.router.url.path

    @rx.var
    def current_page_formatted(self) -> str:
        """
        Returns the current page in a formatted way, if needed.
        This can be expanded to include more complex formatting logic.
        """
        return self.current_page.replace("/", "").capitalize()
    
    @rx.var
    def search_results_not_ready(self) -> bool:
        """
        Indicates whether the search results are ready to be displayed.
        This can be used to show a loading state or skeleton while results are being fetched.
        """
        return True if self.search_input and not self.search_results else False
    
    def submit_search_from_navbar(self, form_data: dict) -> Iterable[Callable]:
        """
        Handles the search submission from the navbar.
        This method can be expanded to include actual search logic.
        """
        search_input = form_data.get("search_input", "")
        yield PageState.setvar("search_input", search_input)
        yield PageState.setvar("search_modal_open", True)
        console.print(f"Search submitted: {search_input}")
        yield PageState.setvar("is_loading", False)

    def default_script_callback(*args, **kwargs) -> Iterable[Callable]:
        """
        Default script callback for handling script calls.
        This can be overridden in specific pages or components.
        """
        console.print(f"Frontend javascript executed.")