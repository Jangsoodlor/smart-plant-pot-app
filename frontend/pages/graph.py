from collections.abc import Callable

import streamlit as st
from components import RadioButtons, TimeSeriesChart


def format_sliders(unit: str) -> Callable:
    def format_func(value):
        if value == 1:
            return f"{value} {unit.title()}"
        return f"{value} {unit.title()}s"

    return format_func


if __name__ == "__main__":
    if "frequency" not in st.session_state:
        st.session_state.frequency = 3
    if "data_range" not in st.session_state:
        st.session_state.data_range = 3

    st.sidebar.header("Select Attribute")
    r = RadioButtons()
    with st.sidebar:
        selected_button = r.buttons
    st.write(f"# Average {RadioButtons.format_func(selected_button)}")

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
        TimeSeriesChart().get_fig(
            x="readTime",
            y=selected_button,
            frequency=st.session_state.frequency,
            data_range=st.session_state.data_range,
        )
    )
