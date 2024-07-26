"""
Create the TableState for the data table
"""
from reflex import State
from typing import Any, Callable, Coroutine


async def _dummy_get_data():
    return [{"id": 1, "name": "Example", "age": 30}]  # Ejemplo de datos


class TableState(State):
    """State for the DataTable"""

    # Constructor para inicializar atributos de instancia
    def __init__(self):
        self._full_data = []
        self._n_items = 0
        self._offset = 0
        self._limit = 7
        self.have_next = False
        self.have_prev = False
        self.loading = True
        self.page_number = 0
        self.total_pages = 0

    # Método para obtener datos
    async def fetch_data(self):
        self.loading = True
        self._full_data = await self._query_method()
        self._n_items = len(self._full_data)
        self.loading = False
        self.__total_pages()
        await self.load_entries()

    # Propiedad para obtener los datos paginados
    @property
    def data(self):
        return self._full_data[self._offset:self._offset + self._limit]

    # Método para cambiar de página
    async def load_entries(self):
        await self._perform_query(self._query_method)

    async def _perform_query(self, query_method: Callable):
        if not self._full_data:
            await self._fetch_data(query_method)
        self.__page_number()

    async def _fetch_data(self, query_method: Callable):
        if query_method is not None:
            self._full_data = await query_method()
        self._n_items = len(self._full_data)

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

    # Cálculo del total de páginas
    def __total_pages(self):
        self.total_pages = (self._n_items // self._limit) + \
            (1 if self._n_items % self._limit else 0)
