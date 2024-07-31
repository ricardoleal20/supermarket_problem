"""
Create the loading component
"""
import reflex as rx


def _loading() -> rx.Component:
    """Loading component"""
    return rx.box(
        rx.box(
            rx.spinner(
                size="3",
                padding_right="2em"
            ),
            rx.heading("Loading..."),
            display="flex",
            align_items="center",
            justify_content="center",
            flex_direction="row",
            width="auto",
            height="auto",
        ),
        width="100%",
        height="100%",
        display="flex",
        # align_items="center",
        justify_content="center",
        position="absolute",
    )


Loading = _loading
