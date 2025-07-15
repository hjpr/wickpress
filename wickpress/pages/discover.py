
import reflex as rx

from ..components.nav_bars import navbar, navbar_side
from ..states.discover import DiscoverState
from ..states.page import PageState


"""
Filters for the discover page.
First we define the filter name, then the state to modify and the state variable.
This allows us to easily add new filters without changing the component.
"""
discover_filters: list[str] = [
    "Trending",
    "New Releases",
    "Popular",
    "Short Stories",
    "Upcoming",
    "Editor's Picks",
    "Most Read",
    "Most Shared",
    "Cyberpunk",
    "Fantasy",
    "Science Fiction",
    "Horror",
    "Romance",
    "Mystery",
    "Thriller"
]

@rx.page(
    route="/discover",
    title="Discover - Wick Press"
)
def discover() -> rx.Component:
    return rx.flex(
        navbar(),

        # Contains side navigation and main content
        rx.flex(

            # Sidebar for navigation
            navbar_side(),

            # Main content container
            rx.flex(

                # Main content area, centered and width-limited
                rx.flex(
                    nav_panel_discover(
                        discover_content(),
                        discover_filters,
                        overflow=True
                    ),
                    flex_direction="column",
                    flex_grow="1",
                    width='100%',
                ),
                flex_direction="column",
                align="center",
                width="100%",
            ),
            flex_direction="row",
            flex_grow="1",
            width="100%",
        ),
        flex_direction="column",
        height="100vh",
        width="100%",
    )

def nav_panel_discover(
        content: rx.Component,
        filters: list[str],
        overflow: bool = False,
        sticky: bool = True
        ) -> rx.Component:
    return rx.flex(

        rx.cond(
            overflow,
            # Horizontally scrolling container for filters that overflow
            rx.flex(
                rx.flex(
                    rx.icon("chevron_left", color="var(--gray-10)"),
                    background_image="linear-gradient(to right, var(--gray-1), var(--gray-1) 60%, transparent)",
                    flex_shrink="0",
                    cursor="pointer",
                    align="center",
                    justify="center", 
                    height="3rem",
                    width="3rem",
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
                    padding="0 3rem",
                    align="center",
                    overflow_x="scroll",
                    scrollbar_width="none"
                ),
                rx.flex(
                    rx.icon("chevron_right", color="var(--gray-10)"),
                    background_image="linear-gradient(to left, var(--gray-1), var(--gray-1) 60%, transparent)",
                    flex_shrink="0",
                    cursor="pointer",
                    align="center",
                    justify="center", 
                    height="3rem",
                    width="3rem",
                    padding="0 0 0 1.5rem",
                    position="absolute",
                    right="0",
                    on_click=rx.call_script(
                        "document.getElementById('nav-filter-container').scrollBy({ left: 350, behavior: 'smooth' })",
                        callback=PageState.default_script_callback
                    ),
                ),
                flex_direction="row",
                border_bottom=rx.breakpoints(
                    xs="1px solid var(--gray-3)",  # For small screens
                    sm="none",
                ),
                position="relative",
                max_width="44rem",
                width="100%",
            ),
            # Horizontally scrolling container for filters that DO NOT overflow
            rx.flex(
                rx.flex(
                    rx.foreach(filters, filter_element),
                    id="nav-filter-container",
                    flex_direction="row",
                    flex_grow="1",
                    gap="1rem",
                    height="3rem",
                    padding="0 1rem",
                    align="center",
                    overflow_x="scroll",
                    scrollbar_width="none"
                ),
                bg="var(--gray-1)",
                box_shadow="0 0.5rem 0.5rem var(--gray-1)",
                flex_direction="row",
                position="sticky" if sticky else "relative",
                top="4.5rem" if sticky else "0",
                max_width="36rem",
                width="100%",
            ),
        ),

        # Main content area
        rx.flex(
            rx.flex(
                rx.heading(DiscoverState.selected_filter),
                bg="var(--gray-1)",
                padding="1.5rem 1rem",
                top="4.5rem",
                user_select="none",
            ),
            content,
            id="discover-content",
            flex_direction="column",
            flex_grow="1",
            max_width='36rem',
            scroll_margin_top="10rem",  # Ensure content is not hidden behind sticky navbar and filters
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
            cursor="pointer",
            size="2",
            user_select="none",
            class_name=rx.cond(
                DiscoverState.selected_filter == filter,
                "ring-3 ring-[var(--gray-6)]",
                ""
            ),
            on_click=[
                DiscoverState.setvar("selected_filter", filter),  # Update selected filter state
                rx.scroll_to(elem_id="discover-content")  # Scroll to discover content
            ]
        ),
        cursor="pointer"
    )

def discover_content() -> rx.Component:
    return rx.flex(
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        mockup_element_post(),
        flex_direction="column",
        flex_grow="1",
        class_name="divide-y divide-[var(--gray-3)]",
    )

def mockup_element_post() -> rx.Component:
    return rx.flex(
        # Profile picture container
        rx.flex(
            rx.skeleton(
                height="3rem",
                width="3rem",
                border_radius="full",
            ),
            flex_direction="column",
            justify="start",
        ),
        # Element content container
        rx.flex(
            rx.skeleton(
                height="1.5rem",
            ),
            rx.skeleton(
                height="5.5rem",
            ),
            rx.skeleton(
                height="1.5rem",
            ),
            flex_direction="column",
            flex_grow="1",
            gap="1rem",
            padding="0 1rem"
        ),
        flex_direction="row",
        flex_grow="1",
        padding="1.25rem 1rem",
    )