"""
Result page.

This page include a button to execute the algorithm and print
the result.

The way to calculate the algorithm is going to be with a button, located on the
top-right side of the page.

On the top-left side, we'll found a selection item, to select the algorithm
to use in this execution (the MIL solver, SA or PSO).

In the middle, we'll include a graph that is going to use three different states:

- State 1:
    Empty. It should literally say that it doesn't have result
- State 2:
    Waiting: With a `Loading` message, we'll wait for the results to come
- State 3:
    Show: It would show the given solution.
    
    ## Example 1:
        Show the solution only with a graphical chart solution

    ## Example 2:
        Allow the user to decide if they want to see a Table or a Chart solution

    ## Example 3:
        As a dashboard, using a 3 items.
            Item 1: The Chart bar
            Item 2: The table of solution
            Item 3: Stats of solution
"""
import reflex as rx
# Local imports
from supermarket_front.components import sidebar_section


@sidebar_section(
    page_title="Solution :: SuperMarket",
    route="/project/solution",
    sidebar_title="Solution",
    sidebar_icon="cpu",
    index_position=2,
)
def run() -> rx.Component:
    """Run the problem using the data provided."""
    return rx.box(

    )
