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

    #! FrontEnd Vars
    have_prev: bool = False
    have_next: bool = False
    loading: bool = True
    page_number: int = 0
    total_pages: int = 0
    data: list[dict[str, int | float | str | bool]] = []

    # Method to change the page
    async def _back_load_entries(self):
        """Load the entries"""
        if not self._full_data:
            await self._fetch_data()
        # Update the page number
        await self._perform_query()
        self.data = self._full_data[self._offset:self._offset + self._limit]

    async def prev_page(self) -> None:
        """Move the data to the previous page"""
        self._offset = max(self._offset - self._limit, 0)
        await self.load_entries()

    async def next_page(self) -> None:
        """Move the data to the next page"""
        if self._offset + self._limit < self._n_items:
            self._offset += self._limit
        await self.load_entries()

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
        await self.load_entries()


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
