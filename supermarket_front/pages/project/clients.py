"""
Page that includes the buyers to appear.

The list would include a button on the top-right side of the page,
that would allow us to create the set of customers.

Also, we'll include three options at the top-left side, being those options:

- Quiet day: Build not so much customers
- Middle day: Build normal customers for the day
- Overcharged day: Make the day heavy and almost without rest for the cashiers
"""
from typing import Any, Callable, Optional, Coroutine
import time
import asyncio
import reflex as rx
# Local imports
from supermarket_front.components import sidebar_section
from supermarket_front.components.datatable import DataTable, DataTableCol, TableState

COLUMNS: list[DataTableCol] = [
    DataTableCol(
        title="Qty of Items",
        type="int",
        description="How many items is going to buy",
        icon="shopping-bag"
    )
]


def get_client_data(*_args, **_kwargs) -> list[dict[str, Any]]:
    """Get the data for the DataTable"""
    time.sleep(2)
    # Then, return the data
    import random  # pylint: disable=C0415
    return [
        {
            "qty_of_items": random.randint(0, 50)
        } for _ in range(0, 100)
    ]


class ClientState(TableState):
    """State for the cashiers"""
    _query_method = get_client_data
    __unique__: bool = True

    def load_entries(self) -> None:
        """..."""
        self._perform_query(get_client_data)

    # @rx.var
    # def data(self) -> list[dict[str, int | float | str | bool]]:
    #     """..."""
    #     return self._data


# class ClientState(rx.State):  # pylint: disable=E0239, R0902
#     """State for the DataTable"""
#     # Set the data
#     data: list[dict[str, str | float | int]] = []
#     _full_data: list[dict[str, Any]] = []
#     _n_items: int = 0
#     # Define the limits for the data
#     _offset: int = 0
#     _limit: int = 7
#     # Define params for the Pages
#     have_next: bool = False
#     have_prev: bool = False
#     # Define a parameter to know if you're loading something or not
#     loading: bool = True
#     _query_method: Callable[
#         [],
#         Coroutine[Any, Any, list[dict[str, Any]]]
#     ] = get_client_data
#     # Define the parameters for the pages
#     page_number: int = 0
#     total_pages: int = 0

#     # //////////////////// #
#     #      PROPERTIES      #
#     # //////////////////// #

#     @property
#     def limit(self) -> int:
#         """Return the limit for the TableState"""
#         return self._limit

#     # //////////////////// #
#     #       SETTERS        #
#     # //////////////////// #

#     @limit.setter
#     def limit(self, new_limit: int) -> None:
#         """Set the limit for the TableState"""
#         self._limit = new_limit

#     # //////////////////// #
#     #       METHODS        #
#     # //////////////////// #

#     async def prev_page(self) -> None:
#         """Move the data to the previous page"""
#         self._offset = max(self._offset - self.limit, 0)
#         await self.load_entries()

#     async def next_page(self) -> None:
#         """Move the data to the next page"""
#         if self._offset + self.limit < self._n_items:
#             self._offset += self.limit
#         await self.load_entries()

#     def __page_number(self) -> None:
#         """Get the page number"""
#         if self._n_items:
#             new_page_number = (
#                 (self._offset // self._limit)
#                 + 1
#                 + (1 if self._offset % self._limit else 0)
#             )
#             # If there's no total pages...
#             if self.total_pages <= 0:  # pylint: disable=W0143
#                 self.have_next = False
#                 self.have_prev = False
#             # If only the new page number is on the limit of the total pages...
#             elif new_page_number >= self.total_pages:  # pylint: disable=W0143
#                 self.have_next = False
#                 self.have_prev = True
#             # If the page number is on the lower limit, then there's no prev but there's
#             # next
#             elif new_page_number <= 1:
#                 self.have_next = True
#                 self.have_prev = False
#             # Then, if we have more time, we have both sides available!
#             else:
#                 self.have_next = True
#                 self.have_prev = True

#             # Update the page number
#             self.page_number = (
#                 (self._offset // self._limit)
#                 + 1
#                 + (1 if self._offset % self._limit else 0)
#             )
#         else:
#             # If there are no elements...
#             self.have_prev = False
#             self.have_next = False
#             self.page_number = 0

#     def __total_pages(self) -> None:
#         """Get the total number of variables"""
#         # Get the total pages
#         self.total_pages = self._n_items // self._limit + (
#             1 if self._n_items % self._limit else 0
#         )

#     # ================= #
#     #    Data methods   #
#     # ================= #

#     async def load_entries(self) -> None:
#         """..."""
#         await self._perform_query(get_client_data)

#     async def _perform_query(self, query_method: Callable) -> None:
#         """Load the entries taking in count the current offset and limit"""

#         print(
#             f"Method {type(self).__name__} has method {query_method.__name__}"
#         )

#         # ensure to have the data first
#         if not self._full_data:
#             await self._fetch_data(query_method)
#         # Then, using a session, obtain the data for this page
#         with rx.session() as _session:
#             # Get only the data to show from the full data
#             self.data = self._full_data[self._offset:self._offset + self._limit]
#         # Update the current page
#         self.__page_number()

#     async def _fetch_data(self, query_method: Callable) -> None:
#         """Fetch data using the query method"""
#         # First, set the status loading to true
#         self.loading = True
#         # Then, await for the method
#         if query_method is not None:
#             if self._full_data:
#                 self._full_data += await query_method()
#             else:
#                 self._full_data = await query_method()  # type: ignore
#         # Then, set the loading to False
#         self.loading = False
#         # Update the N elements that we have
#         self._n_items = len(self._full_data)
#         # Get the total pages
#         self.__total_pages()

#     # ================= #
#     #   Unique method   #
#     # ================= #

#     @classmethod
#     def set_query_method(
#         cls: type["ClientState"],
#         method: Optional[Callable[[],
#                                   Coroutine[Any, Any, list[dict[str, Any]]]]] = None
#     ) -> type["ClientState"]:
#         """Create an unique instance of the TableState"""
#         if cls._full_data:
#             raise RuntimeError(
#                 "We cannot create an unique instance from this TableState, since " +
#                 "it already has information."
#             )

#         setattr(cls, "_query_method", method)
#         return cls


@sidebar_section(
    page_title="Customers :: SuperMarket",
    route="/project/customers",
    sidebar_title="Customers for the day",
    sidebar_icon="shopping-basket",
    index_position=1,
    on_load=ClientState.load_entries
)
def customers_in_store() -> rx.Component:
    """Build the page to handle the 'Tasks', being
    the customers to arrive to the store
    """
    # Set the _query_method
    ClientState.set_query_method(get_client_data)
    # Init the table
    table = DataTable(ClientState)
    table.add_cols(COLUMNS)
    # Return the element
    return rx.box(
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
