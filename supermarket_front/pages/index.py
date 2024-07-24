"""
Homepage for the project
"""
import reflex as rx
# Local imports
from supermarket_front import styles


info = {
    "TITLE": "SuperMarket optimization problem",
    "DESCRIPTION": [
        "This is a Python Project"
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
            # Add the project_introduction
            project_intro(),
            # Add the config
            align="center",
            justify="center",
            spacing="9",
        )
    )

# ====================================== #
#         Add custom information         #
# ====================================== #


def project_intro() -> rx.Component:
    """Initialize the project introduction in different views
    
    - Desktop
    - Table
    - Home
    """
    return rx.center(
        rx.desktop_only(
            __desktop_view()
        ),
        # rx.tablet_only(
        #     ...
        # ),
        # rx.mobile_only(
        #     ...
        # )
    )


def __desktop_view() -> rx.Component:
    """Introduce the desktop view"""
    return rx.box(
        rx.vstack(
            rx.center(
                rx.heading(
                    info["TITLE"],
                    as_="h1"
                ),
                width="100%"
            ),
            # Add a new section
            rx.center(
                rx.vstack(
                    *[rx.text(
                        paragraph,
                        margin="1.5em",
                    ) for paragraph in info["DESCRIPTION"]],
                    padding="5",
                    border_radius=styles.BORDER_RADIUS,
                    background_color=styles.Color.BACKGROUND_SECONDARY,
                    width="100%"
                ),
                width="100%"
            ),
            # Include the button
            __button(),
            width="100%"
        ),
        width="100%"
    )


def __button() -> rx.Component:
    """Include the button to redirect you to the page info"""
    return rx.box(
        rx.center(
            rx.link(
                rx.button(
                    rx.text(
                        "Go to project"
                    ),
                    size="3",
                    border_radius=styles.BORDER_RADIUS,
                    border=styles.BORDER,
                    border_color=styles.Color.PRIMARY,
                    background_color="transparent",
                    cursor="pointer",
                ),
                href="/project/cashier_data"
            )
        ),
        width="100%",
        margin_top="1.5em"
    )
