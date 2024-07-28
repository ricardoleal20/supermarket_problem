"""
Create the loading component
"""
import reflex as rx


def _loading() -> rx.Component:
    """Loading component"""
    return rx.box(
        rx.spacer(),
        rx.center(
            rx.spinner(
                size="3",
                padding_right="2em"
            ),
            rx.heading("Loading..."),
            width="100%",
            height="100%",
        ),
        size="30em",
        width="100%",
        height="100%",
    )


Loading = _loading
