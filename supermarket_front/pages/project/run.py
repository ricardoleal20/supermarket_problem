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
from typing import Any
# External imports
import reflex as rx
# Local imports
from supermarket_front.components import sidebar_section
from supermarket_front.components.timeline import Timeline, TimelineHoverTypes
from supermarket_front import styles

# Create the rx.State for obtaining the data


class SolutionData(rx.State):  # pylint: disable=E0239
    """State to obtain the data when we click the button to obtain a solution"""
    data: list[dict[str, int | float | bool]]

    def restart_data(self) -> None:
        """Restart all the values in the state"""
        self.data = []

    def fetch_data(self) -> None:
        """Fetch the data"""


def calculate_time(num_int: int) -> str:
    """Based on a random number integer, return their hour in the middle of the day."""
    if not 0 <= num_int <= 720:
        raise ValueError("The number must be 0 and 720.")

    base_hour = 8
    total_minutes = num_int
    hours = total_minutes // 60
    minutes = total_minutes % 60

    # Calculate the hour
    hour = base_hour + hours
    return f"2024-07-28T{hour:02}:{minutes:02}:00"


def fetch_solution_data() -> list[dict[str, Any]]:
    """..."""
    # time.sleep(1)
    # Create the data

    import random  # pylint: disable=C0415
    solution: list[dict[str, Any]] = []
    for i in range(0, 5):
        # Define an start randomly
        start = 0
        for _ in range(0, 30):
            end = start + random.randint(5, 20)
            if start >= 720 or end >= 720:
                break

            solution.append({
                "processor": f"Cashier {i}",
                "task": "Client",
                "start": calculate_time(start),
                "end": calculate_time(end),
                "duration": end - start,
                "products": random.randint(5, 50)
            })
            start = end + random.randint(0, 20)
    # Return the solution
    return solution

@sidebar_section(
    page_title="Solution :: SuperMarket",
    route="/project/solution",
    sidebar_title="Solution",
    sidebar_icon="cpu",
    index_position=2,
    on_load=SolutionData.restart_data
)
def run() -> rx.Component:
    """Run the problem using the data provided."""
    # Create the timeline class
    timeline = Timeline()
    # Obtain the data
    data = fetch_solution_data()
    # Set the data to the timeline
    timeline.set_data(data)
    # Set the extra info to show in the hover
    timeline.set_custom_info_in_hover({
        "duration": TimelineHoverTypes.MINUTES,
        "products": " units"
    })

    return rx.box(
        # The header of the problem
        rx.hstack(
            rx.heading(
                "Solve problem",
                as_="h1",
            ),
            rx.spacer(),
            rx.button(
                "Run",
                size="3",
                margin_right="1em",
                width="10em",
                border_radius=styles.BORDER_RADIUS,
                background_color=styles.Color.PRIMARY,
                cursor="pointer",
                _hover={
                    "opacity": "40%"
                }
            ),
            margin_top="1em"
        ),
        # The content
        rx.vstack(
            # Add the component
            timeline.component,
            # Add the text explaining why you should run the algorithm
        ),
        width="100%",
        height="100%"
    )
