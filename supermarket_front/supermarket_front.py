"""
Application definition for the supermarket
"""
import reflex as rx
# Import the pages
from supermarket_front.pages import index, PROJECT_PAGES
from supermarket_front.styles import GENERAL_BACKGROUND_COLOR

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
        "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap",
        "https://fonts.googleapis.com/css2?family=Oxygen:wght@300;400;700&display=swap",
        "/animated_background.css"
    ],
    style={
        "font_family": "Oxygen, sans-serif",
        "font_size": "13px",
        "background": GENERAL_BACKGROUND_COLOR
    }
)
# Add the pages
app.add_page(
    index, title="SuperMarket Problem",
    route="/",
    description="Introduction to the supermarket problem view."
)
for page in PROJECT_PAGES:
    app.add_page(page, **page.__metadata__)
