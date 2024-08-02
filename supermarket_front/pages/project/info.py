"""
Information page.

This includes two tabs:
    #! Tab 1

    This tab includes information about the problem,
    the variables and how each thing affects to the solution.

    #! TAB 2

    This tab includes information about how it was solved, using
    which tool and things like that.
"""
import reflex as rx
# Local imports
from supermarket_front.components import sidebar_section, WIP

@sidebar_section(
    page_title="Problem information :: SuperMarket",
    route="/project/problem/problem_info",
    sidebar_title="Problem description",
    group="Info",
    group_icon="info",
    index_position=3
)
def description() -> rx.Component:
    """Information page"""
    return WIP()


@sidebar_section(
    page_title="Engine used :: SuperMarket",
    route="/project/problem/engine_info",
    sidebar_title="How it was solved",
    group="Info",
    group_icon="info",
)
def how_it_was_solved() -> rx.Component:
    """Information page"""
    return WIP()
