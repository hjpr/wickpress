
import reflex as rx

from .base import BaseState

class UserState(BaseState):
    """
    User object structure:
    {
        'supabase': {
            'id': User ID
            'aud': Audience
            'role': User role
            'email': User email
            'email_confirmed_at': Email confirmation timestamp
            'phone': User phone number
            'confirmed_at': Confirmation timestamp
            'last_sign_in_at': Last sign-in timestamp
            'app_metadata': Application metadata
            'user_metadata': User metadata
            'identities': User identities
            'created_at': Account creation timestamp
            'updated_at': Last update timestamp
            'is_anonymous': Boolean indicating if the user is anonymous
        }
        'wickpress': {
            'id': Supabase User ID (Links across tables)
            'handle': User's handle
            'personal': {
                'first_name': User's first name
                'last_name': User's last name
                'bio': User's biography
                'avatar_url': URL to the user's avatar image
                'cover_url': URL to the user's cover image
                'website': User's personal website URL
                'location': User's location
            }
            'updated_at': Last update timestamp
    }
    """
    user: dict[str, dict[str, str]]

    @rx.var
    def user_opt_in_social(self) -> bool:
        return True if self.user.get("wickpress", {}).get("handle") else False
