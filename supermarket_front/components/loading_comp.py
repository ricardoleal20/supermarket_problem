"""
Create the loading component
"""
import reflex as rx


def _loading() -> rx.Component:
    """Loading component"""
    return rx.box(
        rx.spacer(),
        rx.center(
            rx.heading("Loading..."),
        ),
        width="100%",
        height="100%"
    )


Loading = _loading
