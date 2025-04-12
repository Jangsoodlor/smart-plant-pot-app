import re

import pandas as pd
import plotly.express as px
import streamlit as st

from .api_fetcher import APIFetcher


class RadioButtons:
    __instance = None

    def __init__(self):
        print("New instance")
        self.__buttons = None
        self.__sensor_attr = APIFetcher.get_attributes("sensor")
        self.__weather_attr = APIFetcher.get_attributes("weather")

    @staticmethod
    def format_func(x):
        return "".join(
            [a.title() + " " for a in (re.split(r"(?=[A-Z][^A-Z])", x))]
        ).strip()

    @property
    def buttons(self):
        if self.__buttons is None:
            self.__buttons = st.radio(
                options=[
                    value
                    for value in self.__sensor_attr + self.__weather_attr
                    if value != "readTime"
                ],
                label="Select Attribute",
                label_visibility="collapsed",
                format_func=self.format_func,
            )

        return self.__buttons

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance


class TimeSeriesChart:
    __instance = None

    def __init__(self):
        self.__sensor_attr = APIFetcher.get_attributes("sensor")

    def get_fig(self, x: str, y: str, frequency: int, data_range: int):
        if y in self.__sensor_attr:
            df = APIFetcher.aggregate_data("sensor", frequency, data_range)
        else:
            df = APIFetcher.aggregate_data("weather", frequency, data_range)
        return px.line(data_frame=df, x=x, y=y)

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
