import plotly.express as px
import streamlit as st
from utils import APIFetcher, camel_to_title


class RadioButtons:
    __sensor_attr = APIFetcher.get_attributes("sensor")
    __weather_attr = APIFetcher.get_attributes("weather")

    @classmethod
    def render(cls):
        return st.radio(
            options=[
                value
                for value in cls.__sensor_attr + cls.__weather_attr
                if value != "readTime"
            ],
            label="Select Attribute",
            label_visibility="collapsed",
            format_func=camel_to_title,
        )


class TimeSeriesChart:
    __sensor_attr = APIFetcher.get_attributes("sensor")

    @classmethod
    def get_fig(cls, x: str, y: str, frequency: int, data_range: int):
        if y in cls.__sensor_attr:
            df = APIFetcher.aggregate_data("sensor", frequency, data_range)
        else:
            df = APIFetcher.aggregate_data("weather", frequency, data_range)
        return px.line(data_frame=df, x=x, y=y)
