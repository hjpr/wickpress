
from .base import BaseState
from rich.console import Console

console = Console()

class MessageState(BaseState):
    
    selected_filter: str = "All"