
from .base import BaseState
from loguru import logger

class UserState(BaseState):
    
    def sign_in(self, form_data: dict) -> None:
        logger.info(f"UserState: sign_in called with form_data: {form_data}")