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
from typing import Any
import asyncio
import reflex as rx
# Local imports
from supermarket_front.components import sidebar_section
from supermarket_front.components.datatable import DataTable, DataTableCol, TableState



COLUMNS: list[DataTableCol] = [
    DataTableCol(
        title="Name",
        type="str",
        description="Cashier unique identifier",
        icon="fingerprint"
    ),
    DataTableCol(
        title="Available in the morning",
        type="bool",
        description="Can be in the morning shift",
        # width=300,
        group="Availability",
        icon="sunrise"
    ),
    DataTableCol(
        title="Available in the afternoon",
        type="bool",
        description="Can be in the afternoon shift",
        # width=300,
        group="Availability",
        icon="sunset"
    ),
    # Add the rates
    DataTableCol(
        title="Effectiveness average",
        type="percentage",
        description="How efficient it is in average",
        # width=300,
        icon="percent"
    ),
]


async def get_data(*_args, **_kwargs) -> list[dict[str, Any]]:
    """Get the data for the DataTable"""
    await asyncio.sleep(2)
    # Then, return the data
    import random  # pylint: disable=C0415
    return [
        {
            "name": f"Cashier {i}",
            "available_in_the_morning": True,
            "available_in_the_afternoon": False,
            "effectiveness_average": round(random.random()*100, 3)
        } for i in range(0, 100)
    ]

@sidebar_section(
    page_title="Cashier's :: SuperMarket",
    route="/project/cashier_data",
    sidebar_title="Cashier's info",
    sidebar_icon="user",
    index_position=0,
)
def cashier_data() -> rx.Component:
    """Create and return the DataTable for the cashier data"""
    # Create the state
    state = TableState.unique(method=get_data)
    # Init the table
    table = DataTable(state)
    table.add_cols(COLUMNS)

    # Add the data
    #! STATE
    import random  # pylint: disable=C0415
    table.add_data([{
        "name": f"Cashier {i}",
        "available_in_the_morning": True,
        "available_in_the_afternoon": False,
        "effectiveness_average": round(random.random()*100, 3)
    } for i in range(0, 100)])

    # Convert this table to editable
    table.is_editable = True

    # Return the box with the table component
    return rx.box(
        rx.heading(
            "Cashier info", as_="h1",
            margin_top="1em"
        ),
        # Add a minor spacing
        rx.spacer(),
        rx.center(
            rx.vstack(
                table.component,
                width="100%",
                margin_right="1em",
                margin_top="3em",
                margin_bottom="3em"
            ),
            width="100%",
            # max_height="80%"
        ),
        width="100%"
    )
