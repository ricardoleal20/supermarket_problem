"""
Application definition for the supermarket
"""
import reflex as rx
# Import the pages
from supermarket_front.pages import index

# ========================================== #
#                    APP                     #
# ========================================== #


# Create the app.
app = rx.App(  # pylint: disable=E1102
    theme=rx.theme(
        appearance="dark",
        has_background=True
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"
    ],
    style={
        "font_family": "Montserrat, sans-serif",
        "font_size": "13px",
        "background": rx.color("black", shade=5)
    }
)
# Add the pages
app.add_page(
    index, title="SuperMarket Problem",
    route="/",
    description="Introduction to the supermarket problem view."
)
