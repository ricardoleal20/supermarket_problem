"""
Homepage for the project
"""
import reflex as rx
# Local imports
from supermarket_front import styles


info = {
    "TITLE": "Optimized Flexible Supermarket Solution",
    "DESCRIPTION": [
        "This project aims to optimize supermarket operations by managing various aspects " +
        "like cashier task assignments, FIFO queues, and resource allocation. " +
        "The solution employs advanced mathematical algorithms to improve efficiency " +
        "and reduce operational costs. By leveraging " +
        "PyMath" +
        ", a Python-based tool integrated " +
        "with Rust for high-performance numerical computations, my project offers a robust " +
        "and scalable approach to handling supermarket logistics and operations."
    ]
}


# ====================================== #
#             Index component            #
# ====================================== #


def index() -> rx.Component:
    """Index page. Includes the welcome view for the user
    and a brief description of what's the purpose of the project.
    """
    return rx.box(
        rx.vstack(
            rx.spacer(),
            # Add the project_introduction
            __view(),
            rx.spacer(),
            __footer(),
            justify="center",
            # Add the config
            padding="1em",
            width="100%",
            height="100%",
            min_height="100vh",
        ),
        width="100%",
        height="100%",
        class_name="index_class"
    )

# ====================================== #
#         Add custom information         #
# ====================================== #


def __view() -> rx.Component:
    """Introduce the desktop view"""
    return rx.vstack(
        rx.center(
            rx.heading(
                info["TITLE"],
                rx.desktop_only(
                    font_size="10.5em"
                ),
                rx.mobile_and_tablet(
                    font_size="1em",
                ),
                as_="h1",
                align="center"
            ),
            width="100%",
            height="100%"
        ),
        # Add a new section
        rx.center(
            rx.vstack(
                *[rx.text(
                    paragraph,
                    font_family="Oxygen",
                    font_size="1.5em",
                    margin="1.5em",
                ) for paragraph in info["DESCRIPTION"]],
                rx.text(
                    "For more information, check the ",
                    rx.link(
                        "info",
                        href="/project/problem/problem_info"
                    ),
                    " section in the project.",
                    font_family="Oxygen",
                    font_size="1.5em",
                    margin="1.5em",
                ),
                align="center",
                padding="5",
                border_radius=styles.BORDER_RADIUS,
                background_color=styles.Color.BACKGROUND_SECONDARY,
                width="80%",
                height="100%"
            ),
            width="100%",
            height="100%"
        ),
        # Include the button
        __button(),
        width="100%",
        height="100%",
        align="center",
        justify="center",
    )


def __button() -> rx.Component:
    """Include the button to redirect you to the page info"""
    return rx.box(
        rx.center(
            rx.link(
                rx.button(
                    rx.icon("square-arrow-out-up-right"),
                    rx.text(
                        "Go to project site"
                    ),
                    size="3",
                    border_radius=styles.BORDER_RADIUS,
                    border=styles.BORDER,
                    border_color=styles.Color.PRIMARY,
                    background_color="transparent",
                    cursor="pointer",
                    transition="all 0.15s ease-out allow-discrete",
                    _hover={
                        "background": rx.color("green", shade=5)
                    }
                ),
                href="/project/cashier_data"
            )
        ),
        width="100%",
        height="100%",
        margin_top="1.5em"
    )


def __footer() -> rx.Component:
    """Footer section"""
    return rx.center(
        rx.text("Project made with effort and help of Gato"),
        width="100%",
        height="100%"
    )
