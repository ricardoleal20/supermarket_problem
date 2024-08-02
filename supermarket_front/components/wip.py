"""
Create a `Work in Progress` page
"""
import reflex as rx
from supermarket_front import styles


def _work_in_progress() -> rx.Component:
    """Work in progress page."""
    return rx.center(
        rx.vstack(
            rx.divider(
                width="95%",
                margin_top="1.5em",
            ),
            rx.spacer(),
            rx.hstack(
                rx.icon("pickaxe"),
                rx.heading(
                    "WIP", as_="h1"),
            ),
            rx.text(
                "Page still on work. Sorry for the problems."
            ),
            rx.spacer(),
            rx.divider(
                width="95%",
                margin_bottom="1.5em",
            ),
            width="100%",
            height="15rem",
            border_radius=styles.BORDER_RADIUS,
            background=rx.color("gray", shade=3),
            background_color=rx.color(
                "gray", shade=3),
            align_items="center",
            justify_content="center"
        ),
        margin_top="2em",
        margin_right="1em",
        width="100%",
        height="100%",
        display="flex",
        align_items="center",
        justify_content="center"
    )


WIP = _work_in_progress
