import streamlit as st
from utils import APIFetcher, Units, snake_to_title, parse_time


def write_dashboard(data: dict):
    st.write(f"Last Updated: {parse_time(data['read_time'])}")
    for key, value in data.items():
        if key == "read_time":
            continue
        st.write(f"{snake_to_title(key)}: {value:.2f} {Units.get_unit(key)}")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Welcome to Smart Plant Pot 🪴🌊 App")
    st.write("# Welcome to Smart Plant Pot 🪴🌊 App")
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.write("## Current sensor readings")
        write_dashboard(APIFetcher.get_latest_data("sensor"))
        st.write("## Current weather condition")
        write_dashboard(APIFetcher.get_latest_data("weather"))
    with col2:
        st.write("## Prediction")
        st.write("You should water the plant in x days")
