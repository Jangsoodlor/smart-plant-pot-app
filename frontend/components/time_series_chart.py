import plotly.express as px
import plotly.graph_objects as go
from utils import APIFetcher, snake_to_title, DBAttributes, Units
import pandas as pd
import streamlit as st


class TimeSeriesChart:
    """A class responsible for plotting time series charts."""

    @classmethod
    def append_unit(cls, attribute: str) -> str:
        """Append a unit after a class, if any.

        :param attribute: The attribute that the unit will be appended to.
        :return: A string of the original attribute + the unit, if any.
        """
        unit = Units.get_unit(attribute)
        return (
            f"{snake_to_title(attribute)} ({unit})"
            if unit != ""
            else snake_to_title(attribute)
        )

    @classmethod
    @st.cache_data
    def fetch_and_get_fig(cls, x: str, y: str, frequency: int, data_range: int):
        """Fetch the data and get the graph figure.

        :param x: x-axis of the graoh.
        :param y: y-axis of the graph.
        :param frequency: sample frequency of the data.
        :param data_range: range of the data.
        :return: A graph figure object.
        """
        if y in DBAttributes.SENSOR_ATTR.value and y in DBAttributes.WEATHER_ATTR.value:
            df1 = APIFetcher.aggregate_data("sensor", frequency, data_range)
            df2 = APIFetcher.aggregate_data("weather", frequency, data_range)
            fig = cls.get_multi_line_chart(
                (df1, "Sensor"), (df2, "Weather API"), x=x, y=y
            )
            return fig
        if y in DBAttributes.SENSOR_ATTR.value:
            df = APIFetcher.aggregate_data("sensor", frequency, data_range)
        else:
            df = APIFetcher.aggregate_data("weather", frequency, data_range)
        fig = cls.get_single_line_chart(df, x, y)
        return fig

    @classmethod
    def get_single_line_chart(cls, df: pd.DataFrame, x: str, y: str):
        """Get a line chart with single line.

        :param df: Pandas dataframe.
        :param x: x-axis of the graph.
        :param y: y-axis of the graph.
        :return: A graph figure object.
        """
        fig = px.line(data_frame=df, x=x, y=y)
        cls.__add_fig_legends(x, y, fig)
        return fig

    @classmethod
    def get_multi_line_chart(
        cls, *dataframes: tuple[pd.DataFrame, str], x: str, y: str
    ):
        """Get a line chart with multiple line.

        :param x: x-axis of the graph.
        :param y: y-axis of the graph.
        :return: A graph figure object.
        """
        fig = go.Figure()
        for df, source in dataframes:
            fig.add_trace(
                go.Scatter(
                    x=df[x],
                    y=df[y],
                    mode="lines",
                    name=f"{source}",
                )
            )
        cls.__add_fig_legends(x, y, fig)
        return fig

    @classmethod
    def __add_fig_legends(cls, x, y, fig):
        """Add legends to the graph.

        :param x: x-axis of the graph.
        :param y: y-axis of the graph.
        :param fig: A graph figure object.
        :return: A graph figure object with updated legends.
        """
        return fig.update_layout(
            xaxis_title=snake_to_title(x),
            yaxis_title=f"{cls.append_unit(y)}",
        )
