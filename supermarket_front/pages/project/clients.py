"""
Page that includes the buyers to appear.

The list would include a button on the top-right side of the page,
that would allow us to create the set of customers.

Also, we'll include three options at the top-left side, being those options:

- Quiet day: Build not so much customers
- Middle day: Build normal customers for the day
- Overcharged day: Make the day heavy and almost without rest for the cashiers
"""
from typing import Union
import asyncio
import reflex as rx
# Local imports
from supermarket_front.components import sidebar_section, Loading
from supermarket_front.components.datatable import DataTable, DataTableCol
from supermarket_front.components.table_state import TableState

COLUMNS: list[DataTableCol] = [
    DataTableCol(
        title="Hour of arrival",
        type="int",
        description="Hour of arrival",
        icon="watch"
    ),
    DataTableCol(
        title="Qty of Items",
        type="int",
        description="How many items is going to buy",
        icon="shopping-bag"
    )
]


def calculate_time(num_int: int) -> str:
    """Based on a random number integer, return their hour in the middle of the day."""
    if not 0 <= num_int <= 720:
        raise ValueError("The number must be 0 and 720.")

    base_hour = 8
    total_minutes = num_int
    hours = total_minutes // 60
    minutes = total_minutes % 60

    # Calcula la hora
    hour = base_hour + hours
    return f"{hour:02}:{minutes:02}"


class CustomerState(TableState):
    """State for the cashiers"""
    __unique__: bool = True

    @staticmethod
    async def query_method() -> list[dict[str, Union[int, float, str, bool]]]:
        """Query method for the Cashier State"""
        await asyncio.sleep(1)
        # Then, return the data
        import random  # pylint: disable=C0415
        return [
            {
                "hour_of_arrival": calculate_time(random.randint(0, 720)),
                "qty_of_items": random.randint(0, 50)
            } for _ in range(0, 100)
        ]

    async def load_entries(self) -> None:
        """Method to load the entries of the algorithm"""
        await self._back_load_entries()

    async def fetch_data(self):
        """Fetch the data for the CustomerState"""
        self.data = []
        self._full_data = []
        self.page_number = 0
        self.total_pages = 0
        self.loading = True
        yield
        # Load the entries
        await self.load_entries()

@sidebar_section(
    page_title="Customers :: SuperMarket",
    route="/project/customers",
    sidebar_title="Customers for the day",
    sidebar_icon="shopping-basket",
    index_position=1,
    on_load=CustomerState.fetch_data
)
def customers_in_store() -> rx.Component:
    """Build the page to handle the 'Tasks', being
    the customers to arrive to the store
    """
    # Init the table
    table = DataTable(CustomerState)
    table.add_cols(COLUMNS)
    # Return the element
    return rx.box(
        # Add a minor spacing
        rx.spacer(),
        rx.cond(
            CustomerState.loading,
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
        width="100%"
    )
