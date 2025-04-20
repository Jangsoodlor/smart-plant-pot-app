import pandas as pd
import streamlit as st
from components import TimeSeriesChart, navbar


def init_page():
    st.set_page_config(
        layout="wide", page_title="Watering Prediction | Smart Plant Pot 🪴🌊 App"
    )
    navbar()
    if "show_chart" not in st.session_state:
        st.session_state.show_chart = False
    if "prediction" not in st.session_state:
        st.session_state.prediction = ""


def predict():
    update_prediction("3000 days")
    st.session_state.show_chart = True


def update_prediction(x: str):
    st.session_state.prediction = f"### You should water your plant in {x} days"


def get_prediction_chart(df: pd.DataFrame):
    return TimeSeriesChart.fetch_and_get_fig(
        x="read_time",
        y="soil_moisture",
        frequency=3,
        data_range=3,
    )


if __name__ == "__main__":
    init_page()
    st.write("# Watering Prediction")
    col1, col2 = st.columns((0.45, 0.55))
    with col1:
        soil_moisture = st.text_input(
            label="Please input the desired soil moisture level", key="soil_moisture"
        )
        st.button("Predict", on_click=predict)
    with col2:
        st.write(st.session_state.prediction)
    st.write("## Prediction Graph")
    if st.session_state.show_chart:
        st.plotly_chart(get_prediction_chart(None))
