
import reflex as rx

from .base import BaseState
from reflex.event import EventSpec
from rich.console import Console
from typing import Generator

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
    selected_filter: str = "All"

    @rx.var
    def current_page(self) -> str:
        """
        Separate the url at the "/" so that the base url root can be extracted.
        URL format for the site is e.g. /main-section-name/branch/another-branch/[parameter].
        We're using the main-section-name as the header for our navbar.
        """
        page = self.router.url.path
        page_root = page.split("/")
        return page_root[1] if len(page_root) > 1 else page_root[0]

    @rx.var
    def current_page_formatted(self) -> str:
        """
        Returns the current page in a formatted way, if needed.
        This can be expanded to include more complex formatting logic.
        """
        return self.current_page.capitalize()
    
    @rx.var
    def search_results_not_ready(self) -> bool:
        """
        Indicates whether the search results are ready to be displayed.
        This can be used to show a loading state or skeleton while results are being fetched.
        """
        return True if self.search_input and not self.search_results else False
    
    def submit_search_from_navbar(self, form_data: dict) -> Generator[EventSpec]:
        """
        Handles the search submission from the navbar.
        This method can be expanded to include actual search logic.
        """
        search_input = form_data.get("search_input", "")
        yield PageState.setvar("search_input", search_input)
        yield PageState.setvar("search_modal_open", True)
        console.print(f"Search submitted: {search_input}")
        yield PageState.setvar("is_loading", False)

    def default_script_callback(self) -> None:
        """
        Default script callback for handling script calls with no callback.
        Suppresses logging [Reflex Frontend Exception] errors.
        """
        return None