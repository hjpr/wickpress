
import reflex as rx

from ..states.page import PageState


def nav_panel(content: rx.Component, filters: list[str]) -> rx.Component:
    return rx.flex(

        # Horizontally scrolling container for filters
        rx.flex(
            rx.flex(
                rx.icon("chevron_left", color="var(--gray-10)"),
                background_image="linear-gradient(to right, var(--gray-1), var(--gray-1) 60%, transparent)",
                flex_shrink="0",
                cursor="pointer",
                align="center",
                justify="center", 
                height="3rem",
                width="4rem",
                padding="0 1.5rem 0 0",
                position="absolute",
                on_click=rx.call_script(
                    "document.getElementById('nav-filter-container').scrollBy({ left: -350, behavior: 'smooth' })",
                    callback=PageState.default_script_callback
                ),
            ),
            rx.flex(
                rx.foreach(filters, filter_element),
                id="nav-filter-container",
                flex_direction="row",
                flex_grow="1",
                gap="1rem",
                height="3rem",
                padding="0 3.25rem",
                align="center",
                overflow_x="scroll",
                scrollbar_width="none",
            ),
            rx.flex(
                rx.icon("chevron_right", color="var(--gray-10)"),
                background_image="linear-gradient(to left, var(--gray-1), var(--gray-1) 60%, transparent)",
                flex_shrink="0",
                cursor="pointer",
                align="center",
                justify="center", 
                height="3rem",
                width="4rem",
                padding="0 0 0 1.5rem",
                position="absolute",
                right="0",
                on_click=rx.call_script(
                    "document.getElementById('nav-filter-container').scrollBy({ left: 350, behavior: 'smooth' })",
                    callback=PageState.default_script_callback
                ),
            ),
            flex_direction="row",
            position="relative",
            max_width="44rem",
            width="100%",
        ),

        # Main content area
        rx.flex(
            content,
            flex_direction="column",
            flex_grow="1",
            max_width='36rem',
            width='100%',
        ),
        bg="var(--gray-1)",
        flex_direction="column",
        flex_grow="1", 
        align="center", # Center content horizontally
        padding=rx.breakpoints(
            xs="4.5rem 0 0 0", # When sidebar is hidden
            sm="4.5rem 0 0 4.5rem",
            md="4.5rem 0 0 4.5rem", 
            lg="4.5rem 0 0 4.5rem", 
            xl="4.5rem 0 0 4.5rem" 
        )
    )

def filter_element(filter: str) -> rx.Component:
    return rx.flex(
        rx.badge(
            filter,
            size="2",
            user_select="none"
        ),
        cursor="pointer"
    )