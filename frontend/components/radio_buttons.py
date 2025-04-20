import streamlit as st
from utils import DBAttributes, snake_to_title


class RadioButtons:
    @staticmethod
    def render():
        return st.radio(
            options=set(sorted([
                value
                for value in DBAttributes.SENSOR_ATTR.value
                + DBAttributes.WEATHER_ATTR.value
                if value != "read_time"
            ])),
            label="Select Attribute",
            label_visibility="collapsed",
            format_func=snake_to_title,
        )
