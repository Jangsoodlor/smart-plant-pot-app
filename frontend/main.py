import streamlit as st
from utils import APIFetcher, Units, parse_time, snake_to_title
from components import navbar


def write_dashboard(data: dict):
    st.write(f"Last Updated: {parse_time(data['read_time'])}")
    for key, value in data.items():
        if key == "read_time":
            continue
        st.write(f"{snake_to_title(key)}: {value:.2f} {Units.get_unit(key)}")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Main | Smart Plant Pot 🪴🌊 App")
    navbar()
    st.write("# Welcome to Smart Plant Pot 🪴🌊 App")
    col1, col2 = st.columns(2)
    with col1:
        st.write("## Latest sensor readings")
        write_dashboard(APIFetcher.get_latest_data("sensor"))
    with col2:
        st.write("## Current weather condition")
        write_dashboard(APIFetcher.get_latest_data("weather"))
