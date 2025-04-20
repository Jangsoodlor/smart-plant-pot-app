from collections.abc import Callable

import streamlit as st
from components import RadioButtons, TimeSeriesChart, navbar
from utils import snake_to_title


def format_sliders(unit: str) -> Callable:
    """Format function of the slider

    :param unit: unit of the slider.
    :return: A format function that add unit to the slider's value.
    """

    def format_func(value):
        if value == 1:
            return f"{value} {unit.title()}"
        return f"{value} {unit.title()}s"

    return format_func


if __name__ == "__main__":
    navbar()
    if "frequency" not in st.session_state:
        st.session_state.frequency = 3
    if "data_range" not in st.session_state:
        st.session_state.data_range = 3

    st.sidebar.header("Select Attribute")
    with st.sidebar:
        selected_button = RadioButtons.render()
    st.write(f"# History of {snake_to_title(selected_button)}")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        frequency = st.select_slider(
            "Sampling Frequency",
            options=(i for i in range(1, 25) if 24 % i == 0),
            key="frequency",
            format_func=format_sliders("hour"),
        )

    with col2:
        data_range = st.select_slider(
            "Data Range",
            options=(i for i in list(range(1, 8)) + [15, 30]),
            key="data_range",
            format_func=format_sliders("day"),
        )

    st.plotly_chart(
        TimeSeriesChart.fetch_and_get_fig(
            x="read_time",
            y=selected_button,
            frequency=st.session_state.frequency,
            data_range=st.session_state.data_range,
        )
    )
