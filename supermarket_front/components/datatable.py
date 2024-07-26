"""
Include a DataTable component with custom data
"""
from typing import (
    Any, Optional, TypeVar, Callable,
    Literal, Coroutine
)
from copy import copy
# External imports
from dataclasses import dataclass
import reflex as rx
import pydash as _py

T = TypeVar('T')


def bool_type(value: bool) -> rx.Component:
    """Return a cell with a value"""
    if value is True:
        icon = rx.icon(tag="badge-check", size=25,
                       color=rx.color("green", shade=10))
    else:
        icon = rx.icon(tag="badge", size=25,
                       color=rx.color("red", shade=10))
    # Return the cell showing the icon
    return rx.table.cell(icon)


TYPE_EQUAL: dict[str, Callable[[Any], Any]] = {
    "str": rx.table.cell,
    "bool": bool_type,
    "float": rx.table.cell,
    "int": rx.table.cell,
    "percentage": lambda x: rx.table.cell(f"{x}%"),
}

TYPE_FIELD: dict[str, Callable[["DataTableCol", Any], rx.Component]] = {
    "str": lambda col, value: rx.form.control(rx.input(placeholder=col.description, type=col.type), as_child=True),  # pylint: disable=C0301
    "bool": lambda col, value: rx.center(rx.checkbox(col.description, size="3")),  # pylint: disable=C0301,
    "float": lambda col, value: rx.form.control(rx.input(placeholder=col.description, type="number", default_value=str(value), input_mode="decimal"), as_child=True),  # pylint: disable=C0301
    "int": lambda col, value: rx.form.control(rx.input(placeholder=col.description, type="number", default_value=str(value), input_mode="decimal"), as_child=True),  # pylint: disable=C0301
    "percentage": lambda col, value: rx.form.control(rx.input(placeholder=col.description, type="number", default_value=str(value), input_mode="decimal"), as_child=True),  # pylint: disable=C0301
}


@ dataclass
class DataTableCol:
    """Column for the DataTable."""
    title: str
    type: str
    description: Optional[str] = ""
    icon: Optional[str] = ""
    group: Optional[str] = ""
    width: Optional[int] = None

    @ property
    def as_cell(self) -> rx.Component:
        """Return the DataTable Column as a cell"""
        # Add the info
        cell_info: list[rx.Component] = []
        if self.icon:
            cell_info.append(rx.icon(tag=self.icon, size=18))
        cell_info.append(rx.text(self.title))

        return rx.table.column_header_cell(
            rx.hstack(
                *cell_info,
                align="center",
                spacing="2",
            )
        )


class DataTable:
    """..."""
    _cols: list[DataTableCol]
    _data: list[dict[str, Any]]
    _data_value_type: Any
    _state: type["TableState"]
    _editable: bool
    # Slots
    __slots__ = ["_cols", "_data", "_data_value_type", "_state", "_editable"]

    def __init__(self, state: Optional[type["TableState"]]) -> None:
        # Init the params
        self._cols = []
        self._data = []
        self._editable = False
        # Set the state
        if state is None:
            # Define an unique state here
            self._state = TableState
        else:
            # if getattr(state, "__unique__") is False:
            #     raise RuntimeError(
            #         "The state should be unique. Make sure to " +
            #         "run the `TableState.unique()` and to use the given instance from it."
            #     )
            self._state = state


    def add_cols(self, columns: list[DataTableCol] | DataTableCol) -> None:
        """Add DataTable columns

        Args:
            - cols (list[DataTableCol] | DataTableCol): Column to add
        """
        if isinstance(columns, list):
            self._cols += columns
        else:
            self._cols.append(columns)

    def add_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> None:
        """Include data to show in the data table.

        Args:
            data (list[dict[str, Any]] | dict[str, Any]): Data for the columns
        """
        if isinstance(data, dict):
            data = [data]
        # Iterate over it
        for datum in data:
            self._data.append(datum)

    @property
    def is_editable(self) -> bool:
        """Define if this data table is editable or only to show information about the users.

        Returns:
            - if True, the data can be edited. Otherwise, no.
        """
        return self._editable

    @is_editable.setter
    def is_editable(self, editable: bool) -> None:
        """Define if this data table is editable or only to show information about the users."""
        self._editable = editable

    @property
    def component(self) -> rx.Component:
        """Return the table as Reflex component"""
        # Raise an error if there's no columns
        if not self._cols:
            raise RuntimeError(
                "There are no columns to use to build this component")
        if any(len(datum) != len(self._cols) for datum in self._data):
            raise RuntimeError(
                "At least, one datum in the provided data does not have the correct " +
                "amount of elements for the columns. It needs to have the following keys: " +
                f"{[to_snake_case(col.title) for col in self._cols]}."
            )
        init_flex: list[rx.Component] = []
        # Add the `Add button` if the data table is editable
        if self._editable is True:
            init_flex.append(self.__edit_data({}, "add"))
        init_flex.append(rx.spacer())

        print(f"ID of the instance: {id(self)}")
        print("Name of the state:", self._state.__name__)
        print("Name of the query method:", self._state._query_method.__name__)

        # Return the component at the end
        return rx.fragment(
            rx.flex(
                *init_flex,
                # Add the search params,
                rx.hstack(
                    rx.cond(
                        True,  # State.sort_reverse,
                        rx.icon(
                            "arrow-down-z-a", size=28, stroke_width=1.5, cursor="pointer",
                            # on_click=State.toggle_sort
                        ),
                        rx.icon(
                            "arrow-down-a-z", size=28, stroke_width=1.5, cursor="pointer",
                            # on_click=State.toggle_sort
                        ),
                    ),
                    rx.select(
                        [col.title for col in self._cols],
                        placeholder="Sort By",
                        size="3",
                        # on_change=lambda sort_value: State.sort_values(sort_value),
                    ),
                    rx.input(
                        placeholder="Search here...",
                        size="3",
                        # on_change=lambda value: State.filter_values(value),
                    )
                ),
                spacing="3",
                wrap="wrap",
                width="100%",
                padding_bottom="1em",
            ),
            rx.table.root(
                # Add the header
                self.__data_header(),
                # Show the data,
                rx.table.body(
                    rx.foreach(
                        self._state.data,
                        lambda data: self.__show_data(  # pylint: disable=W0108
                            data)
                    )
                ),
                variant="surface",
                size="3",
                width="100%",
                max_height="80%",
                # overflow="auto"
                on_mount=self._state.load_entries
            ),
            rx.flex(
                rx.hstack(
                    rx.button(
                        "<",
                        cursor=rx.cond(
                            self._state.have_prev,
                            "pointer",
                            "not-allowed"
                        ),
                        color_scheme="crimson",
                        disabled=rx.cond(self._state.have_prev, False, True),
                        on_click=self._state.prev_page
                    ),
                    # Add the middle text
                    rx.text(
                        f"Page {self._state.page_number}/{self._state.total_pages}"
                    ),
                    rx.button(
                        ">",
                        cursor=rx.cond(
                            self._state.have_next,
                            "pointer",
                            "not-allowed"
                        ),
                        color_scheme="crimson",
                        disabled=rx.cond(self._state.have_next, False, True),
                        on_click=self._state.next_page
                    )
                ),
                justify="end",
                spacing="3",
                wrap="wrap",
                width="100%",
                padding_bottom="1em",
            )
        )

    def __data_header(self) -> rx.Component:
        """Create the data header using the given cols"""
        cells = [col.as_cell for col in self._cols]
        # Add the "Actions" cell

        if self._editable is True:
            action = DataTableCol(title="Actions", type="str", icon="cog")
            cells.append(action.as_cell)
        return rx.table.header(
            rx.table.row(*cells)
        )

    def __show_data(self, data: dict[str, Any]) -> rx.Component:
        """..."""
        # Fill the info in the table row
        info: list[rx.Component] = []

        def _data_cell(value: list[str]) -> rx.Component:
            """Get the cell to modify the data of the pair of values: [(str, str)]"""

            as_type = None
            for col in self._cols:
                find_var = rx.cond(
                    to_snake_case(col.title) == value[0],
                    True,
                    False
                )
                if find_var is True:
                    as_type = col
                    break
            return _modify_data(value[1], as_type)

        #! This is expecting to show the default value for each parameter.
        info = [
            rx.foreach(data, _data_cell)
        ]

        row_info: list[rx.Component] = info
        # Add the edit and delete button ONLY if the data table can be edited
        if self._editable is True:
            row_info.append(
                rx.table.cell(
                    rx.hstack(
                        self.__edit_data(data),
                        rx.icon_button(
                            rx.icon("trash-2", size=22),
                            # on_click=lambda: State.delete_customer(
                            #     getattr(user, "id")),
                            size="2",
                            variant="solid",
                            color_scheme="red",
                            cursor="pointer"
                        ),
                    )
                )
            )

        # Return the row with the formatted info
        return rx.table.row(
            *row_info,
            _hover={"bg": rx.color("gray", 3)},
            align="center",
        )

    def __edit_data(
            self,
            data: dict[str, Any],
            as_type: Literal["edit", "add"] = "edit"
    ) -> rx.Component:
        """Edit the data with a dialog component"""
        # Create their own form fields
        form_fields: list[rx.Component] = []
        for col in self._cols:
            # Find their value in the data
            try:
                value = data[to_snake_case(col.title)]
            except:  # pylint: disable=W0702
                value = None
            form_fields.append(_form_field(col, value))

        # Define the trigger
        if as_type == "edit":
            trigger = rx.dialog.trigger(
                rx.button(
                    rx.icon("square-pen", size=22),
                    # rx.text("Edit", size="3"),
                    color_scheme="green",
                    size="2",
                    variant="solid",
                    cursor="pointer",
                    # on_click=lambda: State.get_user(user),
                ),
            )
        else:
            trigger = rx.dialog.trigger(
                rx.button(
                    rx.icon("plus", size=26),
                    rx.text("Add entry", size="4", display=[
                        "none", "none", "block"]),
                    size="3",
                    color_scheme="green",
                    cursor="pointer"
                ),
            )
        return rx.dialog.root(
            trigger,
            # Add the content
            rx.dialog.content(
                rx.hstack(
                    # Add an edit icon
                    rx.badge(
                        rx.icon(tag="square-pen", size=34),
                        color_scheme="green",
                        radius="full",
                        padding="0.65rem",
                    ),
                    # Add the title and description
                    rx.vstack(
                        rx.dialog.title(
                            f"{'Edit' if as_type == 'edit' else 'Add'} datum",
                            as_="h1"
                        ),
                        rx.dialog.description(
                            "Edit the parameters for this specific entry data"
                            if as_type == "edit" else
                            "Add a new entry for this given data"
                        ),
                        spacing="1",
                        height="100%",
                        align_items="start",
                    ),
                    height="100%",
                    spacing="4",
                    margin_bottom="1.5em",
                    align_items="center",
                    width="100%",
                ),
                rx.flex(
                    rx.form.root(
                        rx.flex(
                            # Add the elements of the data
                            *form_fields,
                            direction="column",
                            spacing="3",
                        ),
                        rx.flex(
                            # Close button
                            rx.dialog.close(
                                rx.button(
                                    "Cancel",
                                    variant="soft",
                                    color_scheme="gray",
                                ),
                            ),
                            # Submit button
                            rx.form.submit(
                                rx.dialog.close(
                                    rx.button(
                                        f"{'Update' if as_type == 'edit' else 'Add'} element",
                                        color_scheme="green"
                                    ),
                                ),
                                as_child=True,
                            ),
                            padding_top="2em",
                            spacing="3",
                            mt="4",
                            justify="end",
                        ),
                        # on_submit=State.update_customer_to_db,
                        reset_on_submit=False,
                    ),
                    width="100%",
                    direction="column",
                    spacing="4",
                ),
                max_width=450,
                box_shadow="lg",
                padding="1.5em",
                border=f"2px solid {rx.color('green', 7)}",
                border_radius="25px",
            ),
        )

# ================= #
#    TableState     #
# ================= #


async def _dummy_get_data(*_args, **_kwargs) -> list[dict[str, Any]]:
    """Dummy function to use as default in the TableState"""
    return []


class TableState(rx.State):  # pylint: disable=E0239, R0902
    """State for the DataTable"""
    # Set the data
    _full_data: list[dict[str, Any]] = []
    data: list[dict[str, str | float | int]] = []
    _n_items: int = 0
    # Define the limits for the data
    _offset: int = 0
    _limit: int = 7
    # Define params for the Pages
    have_next: bool = False
    have_prev: bool = False
    # Define a parameter to know if you're loading something or not
    loading: bool = True
    _query_method: Callable[
        [],
        Coroutine[Any, Any, list[dict[str, Any]]]
    ] = _dummy_get_data
    # Define the parameters for the pages
    page_number: int = 0
    total_pages: int = 0

    # //////////////////// #
    #      PROPERTIES      #
    # //////////////////// #

    @property
    def limit(self) -> int:
        """Return the limit for the TableState"""
        return self._limit

    # //////////////////// #
    #       SETTERS        #
    # //////////////////// #

    @limit.setter
    def limit(self, new_limit: int) -> None:
        """Set the limit for the TableState"""
        self._limit = new_limit

    # //////////////////// #
    #       METHODS        #
    # //////////////////// #

    async def prev_page(self) -> None:
        """Move the data to the previous page"""
        self._offset = max(self._offset - self.limit, 0)
        await self.load_entries()

    async def next_page(self) -> None:
        """Move the data to the next page"""
        if self._offset + self.limit < self._n_items:
            self._offset += self.limit
        await self.load_entries()

    def __page_number(self) -> None:
        """Get the page number"""
        if self._n_items:
            new_page_number = (
                (self._offset // self._limit)
                + 1
                + (1 if self._offset % self._limit else 0)
            )
            # If there's no total pages...
            if self.total_pages <= 0:  # pylint: disable=W0143
                self.have_next = False
                self.have_prev = False
            # If only the new page number is on the limit of the total pages...
            elif new_page_number >= self.total_pages:  # pylint: disable=W0143
                self.have_next = False
                self.have_prev = True
            # If the page number is on the lower limit, then there's no prev but there's
            # next
            elif new_page_number <= 1:
                self.have_next = True
                self.have_prev = False
            # Then, if we have more time, we have both sides available!
            else:
                self.have_next = True
                self.have_prev = True

            # Update the page number
            self.page_number = (
                (self._offset // self._limit)
                + 1
                + (1 if self._offset % self._limit else 0)
            )
        else:
            # If there are no elements...
            self.have_prev = False
            self.have_next = False
            self.page_number = 0

    def __total_pages(self) -> None:
        """Get the total number of variables"""
        # Get the total pages
        self.total_pages = self._n_items // self._limit + (
            1 if self._n_items % self._limit else 0
        )

    # ================= #
    #    Data methods   #
    # ================= #

    async def load_entries(self) -> None:
        """..."""
        await self._perform_query(_dummy_get_data)

    async def _perform_query(self, query_method: Callable) -> None:
        """Load the entries taking in count the current offset and limit"""

        print(
            f"Method {type(self).__name__} has method {query_method.__name__}"
        )

        # ensure to have the data first
        if not self._full_data:
            await self._fetch_data(query_method)
        # Get only the data to show from the full data
        self._data = self._full_data[self._offset:self._offset + self._limit]
        # Update the current page
        self.__page_number()

    async def _fetch_data(self, query_method: Callable) -> None:
        """Fetch data using the query method"""
        # First, set the status loading to true
        self.loading = True
        # Then, await for the method
        if query_method is not None:
            if self._full_data:
                self._full_data += await query_method()
            else:
                self._full_data = await query_method()  # type: ignore
        # Then, set the loading to False
        self.loading = False
        # Update the N elements that we have
        self._n_items = len(self._full_data)
        # Get the total pages
        self.__total_pages()

# ================= #
#   Extra methods   #
# ================= #


def to_snake_case(title: str) -> str:
    """Convert a data table column title into snake case"""
    return title.lower().replace(" ", "_")


def _modify_data(value: Any, as_type: DataTableCol | None) -> rx.Component:
    """Create their unique table cell depending on the given type"""
    if as_type is None:
        return rx.table.cell(value)
    # Evaluate the type
    prob_type = TYPE_EQUAL[as_type.type]
    # Then, return the modify equal type
    return prob_type(value)


def _form_field(field: DataTableCol, value: Any) -> rx.Component:
    """Create a form field from a given data component"""
    # Add the info for the title stack of the form
    title_stack: list[rx.Component] = []
    if field.icon:
        title_stack.append(rx.icon(field.icon, size=16, stroke_width=1.5))
    title_stack.append(rx.form.label(field.title))
    # then, match the given type and return the desired field
    if value is None:
        if field.type == "bool":
            value = False
        else:
            value = ""

    return rx.form.field(
        rx.flex(
            # Add an HStack for this field
            rx.hstack(
                *title_stack,
                align="center",
                spacing="2",
            ),
            TYPE_FIELD[field.type](field, value),
            direction="column",
            spacing="1",
        ),
        name=field.title,
        width="100%",
    )
