"""
Timeline component for N tasks and N processors


This would show the processor as the Y axis, and the
task are going to be the elements on the X axis.
"""
from typing import Any, Union
from enum import Enum
# Import the plotly lib, pandas and reflex
import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd
import reflex as rx

# Create the Timeline component


def capitalize(word: str) -> str:
    """Capitalize a word of a phrase
    
    Args:
        - word (str): Word to capitalize

    Returns:
        - Word with the first letter as capital
    """
    return word[0].upper() + word[1::]


class TimelineHoverTypes(Enum):
    """Define the available types for the TimelineHover"""
    STRING = ""
    FLOAT = ""
    INTEGER = ""
    DATE = "|%b %d %Y, %H:%M"
    HOURS = " hours"
    MINUTES = " minutes"
    SECONDS = " seconds"
    PROGRESS = "%"


class Timeline:
    """Timeline component for UI."""
    _data: pd.DataFrame
    _hover_custom_params: dict[str, str]
    _extra_params: dict[str, Any]

    __slots__ = [
        "_hover_custom_params", "_data",
        "_extra_params"
    ]

    def __init__(self) -> None:
        self._data = None  # type: ignore
        self._hover_custom_params = {}
        self._extra_params = {}

    def set_data(self, data: list[dict[str, Any]]) -> None:
        """Set the data to represent and show in the timeline component
        
        Args:
            - data (list[dict[str, Any]]): Data to be displayed on the timeline.
        """
        # Evaluate that all the data is show in a proper way
        #! TODO: TO BE ADDED
        self._data = pd.DataFrame(data)

    def set_extra_params(self, extra_parameters: dict[str, Any]) -> None:
        """Set the extra parameters to show in the figure"""
        self._extra_params = extra_parameters

    def set_custom_info_in_hover(
        self, custom_info: dict[str, Union[TimelineHoverTypes, str]]
    ) -> None:
        """Set the custom info to be show it on the hover info.
        
        Args:
            - custom_info: dict[str, TimelineHoverTypes]: Dictionary with the param to show as the
                key and the formatted type as the TimelineHoverTypes
        """
        element_id = 1
        # Set the custom hover info
        for param, expected_format in custom_info.items():
            # Add the first elements for this param
            self._hover_custom_params[param] = f"<b>{capitalize(param)}</b>:" " %{customdata" + \
                f"[{element_id}]" + "}"
            # Add the expected format
            self._hover_custom_params[param] += expected_format.value if isinstance(
                expected_format, Enum) else expected_format
            # Increase the element id by 1 unit
            element_id += 1

    @property
    def component(self) -> rx.Component:
        """Return the Timeline as component"""

        return rx.box(
            rx.center(
                rx.plotly(
                    data=self._create_timeline_fig(),
                    config={'displaylogo': False},
                )
            ),
            width="100%",
            height="100%"
        )

    def _create_timeline_fig(self) -> Figure:
        """Create the timeline figure"""
        # Create the timeline component
        timeline_fig = px.timeline(
            self._data,
            x_start="start",
            x_end="end",
            y="processor",
            **self._extra_params
        )
        timeline_fig.update_yaxes(autorange="reversed", title_text=None)
        timeline_fig.update_xaxes(
            # tickformat="%H:%M",
            dtick=3600000,  # Miliseconds in an hour
            range=["2024-07-28 07:50", "2024-07-28 12:00"],  # Fixed range
            # fixedrange=True  # Avoid to zoom the timeline
            # Add the rangeselector
            rangeselector={
                "buttons": [
                    {
                        "step": "all"
                    }
                ]
            },
            # Add the rangeslider
            rangeslider={
                "visible": True,
                # Full range
                "range": ["2024-07-28 07:50", "2024-07-28 20:10"],
                "thickness": 0.05
            }
        )
        # Update the info show it in the trace
        timeline_fig.update_traces(
            # Define the custom data
            customdata=self._data[
                ["start"] +
                list(self._hover_custom_params.keys())
            ].values,
            # Define the template
            hovertemplate="<br>".join(
                ["<b>Task information</b><br>",
                 "<b>Processor</b>: %{y}",
                 "<b>Start</b>: %{customdata[0]|%b %d, %Y, %H:%M}",
                 "<b>End</b>: %{x}",
                 *list(self._hover_custom_params.values())
                 ]
            )
        )
        # Delete all the other inputs in the figure
        timeline_fig.update_layout(
            dragmode=False,
            modebar_remove=[
                'zoom', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale',
                'pan', 'select', 'lasso2d', 'zoom2d', 'zoom3d', 'resetCameraDefault3d',
                'resetCameraLastSave3d', 'hoverClosestCartesian', 'hoverCompareCartesian',
                'hoverClosest3d', 'toggleSpikelines', 'toImage', 'resetViews'
            ],
            # paper_bgcolor=""
        )

        # Update the width and heigh
        timeline_fig.update_layout(
            width=1100,
            height=600,
            xaxis={
                "tickmode": 'linear'
            }
        )
        # Return the figure
        return timeline_fig
