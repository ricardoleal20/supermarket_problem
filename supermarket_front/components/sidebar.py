"""
Sidebar component for the entire docs page
"""
import os
import warnings
from typing import Callable, Optional
# Reflex imports
import reflex as rx
# Local imports
from supermarket_front import styles

# Add a dictionary for the SECTIONS
SIDEBAR_SECTIONS: dict[int, dict] = {}
SIDEBAR_REDIRECT: dict[int, rx.Component] = {}


def sidebar(route: str) -> rx.Component:
    """The sidebar.

    Returns:
        The sidebar component.
    """
    # Get all the decorated pages and add them to the sidebar.
    return rx.box(
        rx.desktop_only(
            __sidebar_desktop_view(route),
        ),
        rx.mobile_and_tablet(
            __sidebar_mobile_and_tablet_view(route),
            margin_bottom="1em"
        ),
        # display=["none", "none", "block"],
        position="sticky",
        height="100%",
        top="0px",
        border_right=styles.BORDER,
    )

# =============================================== #
#                  Sidebar Views                  #
# =============================================== #


def __sort_stacks(route: str) -> list[rx.Component]:
    """Sort stacks for the views"""
    stacks: dict[int, rx.Component] = {}
    stacks_group: dict[str, dict] = {}
    for i, section in SIDEBAR_SECTIONS.items():
        # If it is a group, then save it for later
        group = section["group"]
        if group is not None:
            if group in stacks_group:
                if i > stacks_group[group]["index"]:
                    stacks_group[group]["index"] = i
                stacks_group[group]["sections"].append(section)
            else:
                stacks_group[group] = {
                    "index": i,
                    "sections": [section]
                }
            continue
        stacks[i] = sidebar_item(
            text=section["title"],
            url=section["route"],
            active=section["route"] == route,
            icon=section["sidebar_icon"]
        )
    # Add the groups
    for group_name, group_elements in stacks_group.items():
        # Get the icon
        icon = None
        for element in group_elements["sections"]:
            if element["group_icon"]:
                icon = element["group_icon"]
                break
        stacks[group_elements["index"]] = sidebar_grouper(
            group_name, group_elements["sections"], route, icon)
    # Check if you have any SIDEBAR_REDIRECT
    if SIDEBAR_REDIRECT:
        # Add the spacer
        stacks.update({min(SIDEBAR_REDIRECT.keys()) - 1: rx.spacer()})
        stacks.update(SIDEBAR_REDIRECT)

    return [
        stacks[i] for i in sorted(stacks)
    ]


def __sidebar_desktop_view(route: str) -> rx.Component:
    """Desktop view of the Sidebar"""
    # Only take those sidebar section that you need
    sorted_stacks = __sort_stacks(route)
    return rx.box(
        rx.vstack(
            sidebar_header(),
            rx.vstack(
                *sorted_stacks,
                width="100%",
                height="100%",
                overflow_y="auto",
                align_items="flex-start",
                padding="1em",
            ),
            rx.spacer(),
            sidebar_footer(),
            height="100dvh",
        ),
        min_width=styles.SIDEBAR_WIDTH,
        background=styles.Color.BACKGROUND
    )


def __sidebar_mobile_and_tablet_view(route: str) -> rx.Component:
    """Desktop view of the Sidebar"""
    sorted_stacks = __sort_stacks(route)
    return rx.box(
        rx.vstack(
            rx.drawer.root(
                rx.hstack(
                    # Add the button to display the drawer
                    rx.drawer.trigger(
                        rx.button(
                            rx.icon(
                                "menu",
                                size=50,
                                padding_top="1.2em"
                            ),
                            justify="start",
                            color=styles.Color.TEXT_SECONDARY.value,
                        ),
                        background=styles.Color.BACKGROUND.value,
                    ),
                    rx.spacer(),
                    position="fixed",
                    width="100%",
                    height="4em",
                    background=styles.Color.BACKGROUND.value,
                    border_bottom=styles.BORDER,
                ),
                rx.drawer.overlay(z_index="999"),
                # Add the portal to open in this situation.
                rx.drawer.portal(
                    # Add the content
                    rx.drawer.content(
                        rx.vstack(
                            rx.spacer(),
                            rx.vstack(
                                # Add the sidebar
                                rx.hstack(
                                    sidebar_header(include_border=False),
                                    # Add the button to close
                                    rx.flex(
                                        rx.drawer.close(
                                            rx.button(
                                                rx.icon(
                                                    "x",
                                                    size=50
                                                ),
                                            ),
                                            color=styles.Color.TEXT_SECONDARY.value,
                                            background="transparent",
                                        ),
                                        justify="end",
                                        align="center",
                                        right="0",
                                        width="100%",
                                        height="100%",
                                    ),
                                    width="100%",
                                    border_bottom=styles.BORDER
                                ),
                                rx.vstack(
                                    *sorted_stacks,
                                    width="100%",
                                    height="100%",
                                    align_items="flex-start",
                                    padding="1em",
                                ),
                                rx.spacer(),
                                sidebar_footer(),
                                background_color=styles.Color.BACKGROUND,
                                width="100%",
                                height="100%"
                            ),
                            background_color=styles.Color.BACKGROUND,
                            right="auto",
                            width="30em"
                        ),
                    )
                ),
                direction="left",
            ),
            width="100%",
            min_width="0%",
            top="0px",
            background_color=styles.Color.BACKGROUND
        )
    )

# =============================================== #
#               Sidebar components                #
# =============================================== #


def sidebar_header(
    include_border: bool = True
) -> rx.Component:
    """Sidebar header.

    Returns:
        The sidebar header component.
    """
    github_project_url = os.environ.get("GITHUB_PROJECT_URL", "")
    if not github_project_url:
        warnings.warn(
            message="The Github Project URL for the Sidebar is not" +
            " available in the environment variables. Add them as" +
            " `GITHUB_PROJECT_URL` if you want to see it"
        )


    return rx.hstack(
        # The logo.
        rx.heading("SuperMarket", as_="h1"),
        rx.spacer(),
        rx.desktop_only(
            rx.link(
                rx.button(
                    rx.icon("github"),
                    background=styles.Color.BACKGROUND.value,
                    color=styles.Color.BACKGROUND_CONTENT.value,
                    variant="soft",
                    cursor="pointer",
                    border_radius=styles.BORDER_RADIUS,
                    transition="all 0.15s ease-out allow-discrete",
                    _hover={
                        "background": styles.Color.BACKGROUND_SECONDARY.value,
                        "color": styles.Color.PRIMARY.value
                    }
                ),
                href=github_project_url,
            ),
        ),
        align="center",
        width="100%",
        border_bottom=rx.cond(
            include_border,
            styles.BORDER,
            ""
        ),
        padding_x="1em",
        padding_y="2em",
    )


def sidebar_footer() -> rx.Component:
    """Sidebar footer.

    Returns:
        The sidebar footer component.
    """
    github_project_url = os.environ.get("GITHUB_PROJECT_URL", "")
    if not github_project_url:
        warnings.warn(
            message="The Github Project URL for the Sidebar is not" +
            " available in the environment variables. Add them as" +
            " `GITHUB_PROJECT_URL` if you want to see it"
        )
    return rx.center(
        rx.hstack(
        rx.spacer(),
        rx.link(
            rx.text(
                "Portfolio",
                transition="all 0.15s ease-out allow-discrete",
                _hover={
                    "color": styles.Color.PRIMARY.value
                }
            ),
            href="https://portfolio.ricardoleal20.dev",
            color_scheme="gray",
            underline="none",
            _hover={
                "color": styles.Color.PRIMARY.value
            }
        ),
            rx.icon("grip-horizontal", color_scheme="gray", size=20),
        rx.link(
            rx.text(
                "Code",
                transition="all 0.15s ease-out allow-discrete",
                _hover={
                    "color": styles.Color.PRIMARY.value
                }),
            href=github_project_url,
            color_scheme="gray",
            underline="none",
            _hover={
                "color": styles.Color.PRIMARY.value
            }
        ),
        width="100%",
        border_top=styles.BORDER,
        padding="1em",
        ),
        width="100%",
    )


def sidebar_item(
    text: str,
    url: str,
    active: bool,
    icon: Optional[str],
    border: bool = False
) -> rx.Component:
    """Sidebar item.

    Args:
        text: The text of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The sidebar item component.
    """
    if active:
        border_cond = styles.SIDEBAR_BORDER
    else:
        border_cond = rx.cond(
            border,
            styles.SIDEBAR_BORDER,
            "transparent",
        )

    item_info = []
    if icon:
        item_info.append(rx.icon(tag=icon, size=25, mapping_right="0.5em"))
    item_info.append(rx.text(text))

    return rx.link(
        rx.hstack(
            *item_info,
            bg=rx.cond(
                active,
                styles.Color.SIDEBAR_HOVER_BACKGROUND.value,
                "transparent",
            ),
            background_position="center",
            background_size="100% 50%",
            border=border_cond,
            color=rx.cond(
                active,
                styles.Color.TEXT_SECONDARY.value,
                styles.Color.SIDEBAR_TEXT.value,
            ),
            align="center",
            border_radius=styles.BORDER_RADIUS,
            width="100%",
            padding="1em",
            margin_bottom="0.5em",
            transition="all 0.15s ease-in allow-discrete",
            _hover={
                "bg": styles.Color.SIDEBAR_HOVER_BACKGROUND,
                "text": styles.Color.SIDEBAR_TEXT,
                # "background_position": "right left",
                "transition": "background-position 3s ease in-out",
                "background_position": "center",
                "background_size": "100% 50%"
            }
        ),
        href=url,
        width="100%",
        underline="none"
    )


def sidebar_grouper(
    title: str,
    sub_items: list[dict[str, str]],
    route: str,
    icon: Optional[rx.Component] = None,
) -> rx.Component:
    """Create a grouper for the Sidebar sections using an accordion"""
    button_info: list[rx.Component] = []

    if icon:
        button_info.append(
            rx.icon(icon, size=25, mapping_right="0.5em"))
    button_info.append(rx.text(title, size="2"))
    return rx.chakra.accordion(
        rx.chakra.accordion_item(
            rx.chakra.accordion_button(
                rx.hstack(
                    *button_info,
                    rx.box(flex_grow=1,),
                    rx.chakra.accordion_icon(),
                    bg="transparent",
                    color=styles.Color.SIDEBAR_TEXT,
                    align_items="center",
                    border_radius=styles.BORDER_RADIUS,
                    border="transparent",
                    width="100%",
                    _hover={
                        "color": styles.Color.SIDEBAR_HOVER_COLOR.value,
                    }
                )
            ),
            rx.chakra.accordion_panel(
                rx.chakra.accordion(
                    rx.flex(
                        *[
                            sidebar_item(
                                text=sub_item["title"],
                                url=sub_item["route"],
                                active=sub_item["route"] == route,
                                icon=sub_item["sidebar_icon"],
                                border=False,
                            )
                            for sub_item in sub_items
                        ],
                        align_items="start",
                        direction="column",
                    ),
                    allow_multiple=True,
                )
            ),
            width="100%",
            align="left",
            border="transparent",
        ),
        height="75%",
        width="100%",
        allow_multiple=True,
    )

# =============================================== #
#               Sidebar decorators                #
# =============================================== #


def sidebar_section(  # pylint: disable=R0913
    page_title: str,
    route: str,
    *,
    sidebar_title: Optional[str] = None,
    sidebar_icon: Optional[str] = None,
    description: Optional[str] = None,
    meta: Optional[list[str]] = None,
    group: Optional[str] = None,
    group_icon: Optional[str] = None,
    index_position: Optional[int] = None,
    on_load: Optional[Callable] = None
) -> Callable[..., Callable[..., rx.Component]]:
    """@sidebar_section decorator.
    
    It allow us to include extra information about the components, and include
    this as a section.
    
    Args:
        - page_title: Title of the page
        - route: Route of the page (should be complete)
        - sidebar_title: Title of the sidebar section
        - description (Optional): Which description we'll give for this page
        - meta (Optional): Metadata for this page
        - index_position (Optional): The position of this element in the sidebar 
    """

    def wrapper(page_cont: Callable[..., rx.Component]) -> Callable[..., rx.Component]:
        """Internal wrapper"""

        # Create the sidebar_component here
        def sidebar_page() -> rx.Component:
            return rx.hstack(
                sidebar(route),
                rx.box(
                    rx.mobile_and_tablet(
                        margin_top="4.5em"
                    ),
                    rx.vstack(
                        page_cont(),
                    ),
                    # width="100%",
                    # height="100%",
                    flex="1"
                ),
                align="start",
                height="100%",
                # position="relative",
            )

        sidebar_page.__doc__ = page_cont.__doc__
        sidebar_page.__name__ = page_cont.__name__
        # Add this metadata to the sidebar page
        sidebar_page.__metadata__ = {
            "title": page_title,
            "route": route,
            "description": description,
            "meta": meta if meta else [],
        }
        if on_load is not None:
            sidebar_page.__metadata__["on_load"] = on_load
        sidebar_page.__sb_section__ = True

        # Based on the count, get the position of this element on the sidebar
        if index_position is None:
            position = max(SIDEBAR_SECTIONS.keys(), default=0) + 1
        else:
            position = index_position
        SIDEBAR_SECTIONS[position] = {
            "title": sidebar_title if sidebar_title else page_title,
            "route": route,
            "sidebar_icon": sidebar_icon,
            "group": group,
            "group_icon": group_icon,
        }
        return sidebar_page
    # Return the wrapper
    return wrapper

# =============================================================== #
# Sidebar helpers                                                 #
# =============================================================== #


def sidebar_redirect(
    sidebar_title: str,
    to_path: str,
    sidebar_icon: Optional[str],
    index_position: int = int(1e6)
) -> None:
    """Add a redirect page element in the sidebar"""
    # Create their sidebar item
    item = sidebar_item(
        sidebar_title, to_path,
        False, sidebar_icon,
    )
    # Add this to the SIDEBAR_REDIRECT
    SIDEBAR_REDIRECT[index_position] = item
