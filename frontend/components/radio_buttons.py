import streamlit as st
from utils import camel_to_title, DBAttributes


class RadioButtons:
    @staticmethod
    def render():
        return st.radio(
            options=[
                value
                for value in DBAttributes.SENSOR_ATTR.value
                + DBAttributes.WEATHER_ATTR.value
                if value != "readTime"
            ],
            label="Select Attribute",
            label_visibility="collapsed",
            format_func=camel_to_title,
        )
