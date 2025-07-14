
import reflex as rx

from ..states.page import PageState

def search_modal_for_navbar() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.flex(
                rx.button(
                    rx.icon("search", size=18),
                    loading=PageState.is_loading,
                    cursor="pointer",
                    size="1",
                    variant="ghost",
                    _hover={"bg": "none"}
                ),
                align="center",
                justify="center",
                height="100%",
                width='2rem',
            )
        ),
        rx.dialog.content(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.icon(
                            "search",
                            color="var(--gray-11)",
                            size=18
                        ),
                        align="center",
                        justify="center",
                        height="100%",
                        width="3rem",
                    ),
                    rx.flex(
                        rx.text_field(
                            placeholder="Writers, series, posts, tags...",
                            value=PageState.search_input,
                            bg="none",
                            border="none",
                            box_shadow="none",
                            outline="none",
                            size="3",
                            type="search",
                            width="100%",
                            _focus_within={
                                "outline": "none",
                                "box_shadow": "none"
                            },
                            on_change=PageState.setvar("search_input").debounce(600),
                        ),
                        align="center",
                        width="100%",
                    ),
                    rx.button(
                        rx.text("Cancel"),
                        cursor="pointer",
                        size="2",
                        variant="soft",
                        on_click=[
                            PageState.setvar("search_input", ""),
                            PageState.setvar("search_modal_open", False)
                        ],
                    ),
                    align="center",
                    height="3rem",
                    padding="2rem 1rem 2rem 1rem",
                    position="sticky",
                    top="0",
                    width="100%",
                ),
                rx.separator(
                    z_index="10",
                ),
                rx.scroll_area(
                    skeleton_search_results(),
                    padding="1rem",
                    width="100%",
                ),
                flex_direction="column",
                height="36rem",
            ),
            padding="0 0 0 0",
            on_pointer_down_outside=PageState.setvar("search_modal_open", False),
        ),
        open=PageState.search_modal_open,
    )

def search_results() -> rx.Component:
    return rx.flex(
        # Image placeholder
        rx.flex(
            bg="var(--gray-1)",
            height='3rem',
            width='3rem',
        ),
        # Contains element text
        rx.flex(
            rx.flex(
                rx.text("Element Name", size="3", weight="medium"),
            ),
            rx.flex(
                rx.text("Type", size="2", weight="light"),
                rx.text("-", size="2", weight="light"),
                rx.text("Subgroup", size="2", weight="light"),
                rx.text("-", size="2", weight="light"),
                rx.text("Subscribers", size="2", weight="light"),
                gap="0.5rem",
            ),
            flex_direction="column",
            justify="center",
            padding="0 1rem",
        ),
        border_radius="0.5rem",
        cursor="pointer",
        _hover={
            "bg":"var(--gray-3)",
        },
        padding="1rem",
        width="100%",
    )

def render_trending_topics(topic: dict) -> rx.Component:
    return rx.flex(
        # Image placeholder
        rx.flex(
            rx.icon("trending-up"),
            bg="var(--gray-1)",
            align="center",
            justify="center",
            height='3rem',
            width='3rem',
        ),
        # Contains element text
        rx.flex(
            rx.flex(
                rx.text(f"{topic["name"]}", size="3", weight="medium"),
            ),
            flex_direction="column",
            justify="center",
            padding="0 1rem",
        ),
        border_radius="0.5rem",
        cursor="pointer",
        _hover={
            "bg":"var(--gray-3)",
        },
        padding="1rem",
        width="100%",
    )

def skeleton_search_element() -> rx.Component:
    return rx.flex(
        # Image placeholder
        rx.skeleton(
            height='3rem',
            width='3rem',
        ),
        # Contains element text
        rx.flex(
            rx.skeleton(
                width="100%",
            ),
            rx.skeleton(
                width="100%",
            ),
            gap="0.5rem",
            flex_direction="column",
            justify="center",
            padding="0 1rem",
            width="100%",
        ),
        padding="1rem",
        width="100%",
    )

def skeleton_search_results() -> rx.Component:
    return rx.cond(
        PageState.search_results_not_ready,
        rx.flex(
            skeleton_search_element(),
            skeleton_search_element(),
            skeleton_search_element(),
            skeleton_search_element(),
            skeleton_search_element(),
            skeleton_search_element(),
            flex_direction="column",
        ),
        rx.foreach(
            PageState.trending_topics,
            render_trending_topics
        )
    )