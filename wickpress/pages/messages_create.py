
import reflex as rx


from ..components.nav_bars import navbar, navbar_side
from ..components.protected import login_protected
from ..components.popovers import message_participant_popover
from ..states.chat import ChatState, CreateChatState

@rx.page(
    route="/messages/create",
    title="Create Chat - Wick Press",
)
@login_protected
def messages_create() -> rx.Component:
    return rx.flex(
        navbar(),

        # Contains side navigation and main content
        rx.flex(

            # Sidebar for navigation
            navbar_side(),

            # Main content container
            rx.flex(

                # Main content area
                rx.flex(

                    # Centered container
                    rx.flex(
                        rx.flex(
                            rx.flex(
                                rx.flex(
                                    rx.cond(
                                        CreateChatState.is_group_chat,
                                        rx.heading("Create New Group Chat"),
                                        rx.heading("Create New Chat"),
                                    ),
                                    width="100%"
                                ),
                                rx.button(
                                    rx.text("Cancel"),
                                    type="button",
                                    cursor="pointer",
                                    size="2",
                                    variant="soft",
                                    on_click=rx.redirect("/messages")
                                ),
                                align="center",
                                padding="1rem",
                                position="sticky",
                                top="0",
                                width="100%",
                            ),
                            rx.separator(
                                z_index="10",
                            ),
                            rx.form(
                                rx.flex(
                                    # 'To' field embedded in popover trigger
                                    rx.flex(
                                        message_participant_popover(),
                                        rx.tooltip(
                                            rx.button(
                                                rx.icon("contact", size=16),
                                                rx.text("Contacts"),
                                                variant="soft",
                                                cursor="pointer"
                                            ),
                                            content="Contacts"
                                        ),
                                        border_bottom="1px solid var(--gray-3)",
                                        padding="1rem",
                                        gap="1rem",
                                        width="100%"
                                    ),
                                    # User selected members for group chat
                                    rx.cond(
                                        ChatState.participants_selected,
                                        rx.flex(
                                            rx.flex(
                                                rx.text("Sending to:", size="2"),
                                                align="center",
                                                margin_right="1rem"
                                            ),
                                            rx.foreach(
                                                ChatState.participants_selected,
                                                participants_selected_render
                                            ),
                                            border_bottom="1px solid var(--gray-3)",
                                            padding="1rem",
                                            width="100%"
                                        ),
                                    ),
                                    # Group chat options
                                    rx.cond(
                                        CreateChatState.is_group_chat,
                                        rx.flex(
                                            rx.flex(
                                                rx.input(
                                                    placeholder="Group Name",
                                                    name="group_name",
                                                    size="2",
                                                    width="100%"
                                                ),
                                                flex_grow="1",
                                                width="100%"
                                            ),
                                            rx.flex(
                                                rx.text_area(
                                                    placeholder="Group Description (Optional)",
                                                    name="group_description",
                                                    rows="4",
                                                    size="2",
                                                    width="100%"
                                                ),
                                                flex_grow="1",
                                                width="100%"
                                            ),
                                            flex_direction="column",
                                            border_bottom="1px solid var(--gray-3)",
                                            padding="1rem",
                                            gap="1rem",
                                        ),
                                    ),
                                    rx.flex(
                                        rx.text_area(
                                            placeholder="Message",
                                            name="message",
                                            rows="8",
                                            size="2",
                                            width="100%"
                                        ),
                                        border_bottom="1px solid var(--gray-3)",
                                        flex_grow="1",
                                        padding="1rem",
                                        width="100%"
                                    ),
                                    rx.flex(
                                        rx.button(
                                            rx.icon("send", size=16),
                                            rx.text("Send")
                                        ),
                                        justify="end",
                                        padding="1rem",
                                        width="100%"
                                    ),
                                    flex_direction="column",
                                    flex_grow="1",
                                    width="100%"
                                ),
                                on_submit=CreateChatState.send_message
                            ),
                            flex_direction="column",
                            max_width="36rem",
                            width="100%"
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
                        ),
                    ),
                    # Panel with header and filters

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

def participants_selected_render(participant: dict) -> rx.Component:
    """
    Renders small badge of a selected user to allow into chat.
    """
    return rx.flex(
        rx.text(f"@{participant.get('handle')}", size="2"),
        rx.center(
            rx.icon("x", size=14),
            height="1.25rem",
            width="1.25rem",
            border_radius="calc(infinity * 1px)",
            cursor="pointer",
            _hover={
                "bg": "var(--gray-4)"
            },
            on_click=ChatState.remove_participants(participant)
        ),
        align="center",
        border="1px solid var(--gray-3)",
        border_radius="calc(infinity * 1px)",
        padding="0.25rem 0.5rem",
        gap="0.5rem",
    )