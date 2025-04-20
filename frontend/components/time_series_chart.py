import plotly.express as px
import plotly.graph_objects as go
from utils import APIFetcher, snake_to_title, DBAttributes, Units
import pandas as pd
import streamlit as st


class TimeSeriesChart:
    @classmethod
    def append_unit(cls, attribute: str):
        unit = Units.get_unit(attribute)
        return (
            f"{snake_to_title(attribute)} ({unit})"
            if unit != ""
            else snake_to_title(attribute)
        )

    @classmethod
    @st.cache_data
    def get_fig(cls, x: str, y: str, frequency: int, data_range: int):
        if y in DBAttributes.SENSOR_ATTR.value and y in DBAttributes.WEATHER_ATTR.value:
            df1 = APIFetcher.aggregate_data("sensor", frequency, data_range)
            df2 = APIFetcher.aggregate_data("weather", frequency, data_range)
            fig = cls.__get_multi_line_chart((df1, "Sensor"), (df2, "API"), x=x, y=y)
        else:
            fig = cls.__get_single_line_chart(x, y, frequency, data_range)
        fig.update_layout(
            xaxis_title=snake_to_title(x),
            yaxis_title=f"{cls.append_unit(y)}",
        )
        return fig

    @classmethod
    def __get_single_line_chart(
        cls, x: str, y: str, frequency: int, data_range: int
    ) -> go.Figure:
        if y in DBAttributes.SENSOR_ATTR.value:
            df = APIFetcher.aggregate_data("sensor", frequency, data_range)
        else:
            df = APIFetcher.aggregate_data("weather", frequency, data_range)
        fig = px.line(data_frame=df, x=x, y=y)
        return fig

    @classmethod
    def __get_multi_line_chart(
        cls, *dataframes: tuple[pd.DataFrame, str], x: str, y: str
    ):
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
        return fig
