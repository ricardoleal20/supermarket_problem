"""
Project pages
"""
import reflex as rx
# Import the sidebar section
from supermarket_front.components.sidebar import sidebar_redirect
# Local imports
from supermarket_front.pages.project.cashier_data import (
    cashier_data, cashier_rates_data
)
from supermarket_front.pages.project.run import run
from supermarket_front.pages.project.info import description, how_it_was_solved


# Add the redirect element
sidebar_redirect(
    sidebar_title="Go home",
    to_path="/",
    sidebar_icon="arrow-big-left",
)


PROJECT_PAGES = [
    cashier_data,
    cashier_rates_data,
    run,
    description, how_it_was_solved
]
