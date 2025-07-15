
from .base import BaseState

class DiscoverState(BaseState):
    """State for the Discover page."""
    
    selected_filter: str = "Trending"