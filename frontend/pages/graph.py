from APIFetcher import APIFetcher
import plotly.express as px
import streamlit as st

if __name__ == "__main__":
    if "frequency" not in st.session_state:
        st.session_state.frequency = "3 hours"
    if "data_range" not in st.session_state:
        st.session_state.data_range = "3 days"

    df = APIFetcher.aggregate_data(
        "sensor",
        int(st.session_state.frequency.split()[0]),
        int(st.session_state.data_range.split()[0]),
    )

    st.sidebar.header("Select Attribute")
    with st.sidebar:
        radio_btn = st.radio(
            options=[col for col in df.columns if col != "readTime"],
            label="Select Attirbute",
            label_visibility="collapsed",
        )

    st.write(f"# Average {radio_btn} every 3 hours")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        frequency = st.select_slider(
            "Sampling Frequency",
            options=(f"{i} hours" for i in range(1, 25) if 24 % i == 0),
            key="frequency",
        )

    with col2:
        data_range = st.select_slider(
            "Data Range", options=(f"{i} days" for i in list(range(1, 8)) + [15, 30]), key="data_range"
        )

    fig = px.line(data_frame=df, x="readTime", y=radio_btn)
    st.plotly_chart(fig)
