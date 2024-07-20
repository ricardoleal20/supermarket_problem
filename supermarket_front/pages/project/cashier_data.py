"""
Cashier Data page.

Include a DataTable for the cashier with available options to modify.

This would allow us to include:

1. Add an extra Cashier
2. Modify the following parameters from existing cashiers:
    - name: Cashier Name
    - available_morning: Available to work in the morning
    - service_rate_morning: Service rate for the morning
    - available_afternoon: Available to work in the afternoon
    - service_rate_afternoon: Service rate for the afternoon

The morning time is:
    - From 8 am to 2 pm
The afternoon time is:
    - From 2 pm to 8 pm
"""
import reflex as rx
# Local imports
from supermarket_front.components import sidebar_section


@sidebar_section(
    page_title="Cashier's :: SuperMarket",
    route="/project/data",
    sidebar_title="Cashier's info",
    group="Cashier's Data",
    group_icon="user",
    index_position=0,
)
def cashier_data() -> rx.Component:
    """Create and return the DataTable for the cashier data"""
    return rx.box(

    )


@sidebar_section(
    page_title="Cashier's Rates :: SuperMarket",
    route="/project/rates",
    sidebar_title="Cashier's rates",
    group="Cashier's Data",
    group_icon="user"
)
def cashier_rates_data() -> rx.Component:
    """Create and return the DataTable for the cashier data"""
    return rx.box(

    )
