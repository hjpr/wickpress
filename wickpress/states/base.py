
import reflex as rx

from functools import wraps
from rich.console import Console
from suplex import Suplex

console = Console()

class BaseState(Suplex):
    pass