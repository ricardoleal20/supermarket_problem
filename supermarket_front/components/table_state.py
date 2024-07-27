"""
Create the TableState for the data table
"""
# Reflex imports
import reflex as rx



async def _dummy_get_data():
    return [{"id": 1, "name": "Example", "age": 30}]  # Ejemplo de datos


class TableState(rx.State):  # pylint: disable=E0239, R0902
    """State for the DataTable"""
    #! BackEnd Vars
    _full_data: list[dict[str, int | float | str | bool]] = []
    _n_items: int = 0
    _limit: int = 5
    _offset: int = 0
    _sort_value: str = ""

    #! FrontEnd Vars
    have_prev: bool = False
    have_next: bool = False
    loading: bool = True
    page_number: int = 0
    total_pages: int = 0
    sort_reverse: bool = False
    data: list[dict[str, int | float | str | bool]] = []

    # Method to sort the data based on a parameter given
    async def sort_values(self, sort_value: str) -> None:
        """Sort the values base on the sort parameter"""
        if sort_value and sort_value != "-":
            self.data = list(sorted(
                self.data,
                key=lambda val: val[to_snake_case(sort_value)],
                reverse=self.sort_reverse
            ))
            # Change the sort value parameter
            self._sort_value = sort_value
        elif sort_value == "-":
            self.data = self._full_data[self._offset:self._offset + self._limit]
            self._sort_value = ""

    async def filter_values(self, filter_param: str) -> None:
        """Filter the values given a search parameter"""

    async def toggle_sort(self) -> None:
        """Change the sort direction"""
        self.sort_reverse = not self.sort_reverse
        await self.sort_values(self._sort_value)

    # Method to move the page
    async def prev_page(self) -> None:
        """Move the data to the previous page"""
        self._offset = max(self._offset - self._limit, 0)
        await self._back_load_entries()

    async def next_page(self) -> None:
        """Move the data to the next page"""
        if self._offset + self._limit < self._n_items:
            self._offset += self._limit
        await self._back_load_entries()

    async def set_limit(self, limit: int) -> None:
        """Define a new limit for the table state"""
        if limit:
            self._limit = int(limit)
        else:
            self._limit = 5
        # Recharge the page limit
        self.__total_pages()
        self.__page_number()
        await self._back_load_entries()

    # Method to change the page
    async def _back_load_entries(self):
        """Load the entries in the backend"""
        if not self._full_data:
            await self._fetch_data()
        # Update the page number
        await self._perform_query()
        self.data = self._full_data[self._offset:self._offset + self._limit]
        # IF there's a sort value, change it
        if self._sort_value:
            await self.sort_values(self._sort_value)

    async def _perform_query(self):
        self.__page_number()

    async def _fetch_data(self):
        # Start the loading mode...
        self.loading = True
        self._full_data = await self.query_method()
        # Once you've got all the full data, perform minor changes
        self._n_items = len(self._full_data)
        self.loading = False
        self.__total_pages()
        # End waiting for the load entries
        await self._back_load_entries()


    # Cálculo de la página actual
    def __page_number(self):
        if self._n_items:
            self.page_number = (self._offset // self._limit) + 1
            self.have_prev = self._offset > 0
            self.have_next = self._offset + self._limit < self._n_items
        else:
            self.page_number = 0
            self.have_prev = False
            self.have_next = False

    # Get the total pages
    def __total_pages(self):
        self.total_pages = (self._n_items // self._limit) + \
            (1 if self._n_items % self._limit else 0)

# ===================== #
#     Extra methods     #
# ===================== #


def to_snake_case(title: str) -> str:
    """Convert a data table column title into snake case"""
    return title.lower().replace(" ", "_")
