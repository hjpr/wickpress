import reflex as rx
import os

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_key")
api_url = os.getenv("api_url")
jwt_secret = os.getenv("jwt_secret")

config = rx.Config(
    app_name="wickpress",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    suplex={
        "api_url": api_url,
        "api_key": api_key,
        "jwt_secret": jwt_secret,
        "let_jwt_expire": False, # (Optional: Default is False) Specify if tokens auto refresh. Can set to True for tighter/manual control of token refresh
        "cookie_max_age": 3600, # (Optional: Default = None) Seconds until cookie expires, otherwise is a session cookie.
    },
    show_built_with_reflex=False,
    telemetry_enabled=False
)