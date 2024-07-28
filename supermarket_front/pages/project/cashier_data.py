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
import asyncio
import reflex as rx
# Local imports
from supermarket_front.components import sidebar_section, Loading
from supermarket_front.components.datatable import DataTable, DataTableCol
from supermarket_front.components.table_state import TableState, DataModel



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


class CashierModel(DataModel):
    """Model for the Cashier data"""
    name: str
    available_in_the_morning: bool
    available_in_the_afternoon: bool
    effectiveness_average: float

class CashierState(TableState):
    """State for the cashiers"""
    __unique__: bool = True

    @staticmethod
    async def query_method() -> list[dict[str, int | float | str | bool]]:
        """Query method for the Cashier State"""
        await asyncio.sleep(1)
        # Then, return the data
        import random  # pylint: disable=C0415
        return [
            {
                "name": f"Cashier {i}",
                "available_in_the_morning": True,
                "available_in_the_afternoon": False,
                "effectiveness_average": round(random.random()*100, 3)
            } for i in range(0, 10)
        ]

    @property
    def data_model(self) -> type[CashierModel]:
        """Return the data model"""
        return CashierModel

    async def load_entries(self) -> None:
        """Method to load the entries of the algorithm"""
        await self._back_load_entries()

    async def fetch_data(self):
        """Fetch data method"""
        self.data = []
        self._full_data = []
        self.page_number = 0
        self.total_pages = 0
        self.loading = True
        yield
        # Load the entries
        await self.load_entries()

@sidebar_section(
    page_title="Cashier's :: SuperMarket",
    route="/project/cashier_data",
    sidebar_title="Cashier's info",
    sidebar_icon="user",
    index_position=0,
    on_load=CashierState.fetch_data
)
def cashier_data() -> rx.Component:
    """Create and return the DataTable for the cashier data"""
    # Init the table
    table = DataTable(CashierState)
    table.add_cols(COLUMNS)
    # Add the data model
    table.add_data_model(CashierModel)
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
        rx.cond(
            CashierState.loading,
            Loading(),
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
        ),
        width="100%",
        height="100%",
    )
