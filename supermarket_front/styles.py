"""
Styles for the app.
"""
from enum import Enum
# Reflex import
import reflex as rx


class Color(Enum):
    """Include the palette of colors"""
    PRIMARY = rx.color("teal", 5)
    SECONDARY = rx.color("orange", 7)
    BACKGROUND = "#1E1E1E"
    BACKGROUND_CONTENT = "#F7F6F6"
    BACKGROUND_SECONDARY = rx.color("gray", shade=3)
    TEXT = "black"
    TEXT_SECONDARY = "white"
    # SideBar Colors
    SIDEBAR_TEXT = rx.color("mauve", 11)
    SIDEBAR_HOVER_COLOR = rx.color("teal", 10)
    SIDEBAR_HOVER_BACKGROUND = rx.color("teal", 5)


class TextSizes(Enum):
    """Include all the available sizes for the text"""
    HEADING_H1 = "3em"
    HEADING_H2 = "2em"
    HEADING_H3 = "1.7em"
    LINKS_TEXT = "1.2em"
    BODY_HOME_TEXT = "1.5em"
    SECTION_HEADING = "2.5em"
    CARD_HEADER = "1.2em"
    CARD_BODY = "1em"
    # This are the MOBILE sizes
    HEADING_H1_MOBILE = "2em"
    HEADING_H2_MOBILE = "1.5em"
    HEADING_H3_MOBILE = "1.3em"
    BODY_HOME_TEXT_MOBILE = "1.3em"
    BODY_HOME_LITTLE_TEXT_MOBILE = "1em"


BORDER_RADIUS = "0.375rem"
BORDER = f"1px solid {rx.color('gray', 6)}"
CONTENT_WIDTH_VW = "90vw"
SIDEBAR_WIDTH = "20em"
SIDEBAR_BORDER = f"0.5px solid {rx.color('gray', 6)}"
