"""
Create the loading component
"""
import reflex as rx

def _loading() -> rx.Component:
    """Loading component"""
    return rx.hstack(
        rx.desktop_only(
            __desktop_view()
        ),
        rx.mobile_and_tablet(
            __mobile_view()
        )
    )


def __desktop_view() -> rx.Component:
    loading_box = __define_loading_box()
    return rx.box(
        loading_box,
        width="100%",
        height="100%",
        display="flex",
        align_items="center",
        justify_content="center",
        position="absolute",
        top=-30,
        left=150,
    )


def __mobile_view() -> rx.Component:
    """..."""
    loading_box = __define_loading_box()
    return rx.box(
        loading_box,
        width="100%",
        height="100%",
        display="flex",
        align_items="center",
        justify_content="center",
        position="absolute",
        top=0,
        left=0,
    )


def __define_loading_box() -> rx.Component:
    """Define the loading component and the spin"""
    return rx.box(
        rx.spinner(
            size="3",
            padding_right="2em"
        ),
        rx.heading("Loading..."),
        display="flex",
        align_items="center",
        justify_content="center",
        flex_direction="row",  # Ensure that they are defined as a row
        # Adjust the content to the width and the height
        width="100%",
        height="100%",
    )


Loading = _loading
