import streamlit as st
from components import TimeSeriesChart, navbar
from utils import APIFetcher


@st.dialog("Invalid Request")
def error_modal(reason: str):
    st.write(reason)
    st.write("Please enter float or integer value.")


def init_page() -> None:
    """Initialise the page"""
    st.set_page_config(
        layout="wide", page_title="Watering Prediction | Smart Plant Pot 🪴🌊 App"
    )
    navbar()
    if "show_chart" not in st.session_state:
        st.session_state.show_chart = False
    if "prediction" not in st.session_state:
        st.session_state.prediction = '## Click "Predict" to get prediction'


def predict() -> None:
    """Get the prediction result and update the page accordingly"""
    try:
        duration, old_data, predictions, upper, lower = (
            APIFetcher.get_soil_moisture_prediction(st.session_state.soil_moisture)
        )
        st.session_state.prediction = f"## {duration}"
        st.session_state.show_chart = True
        st.session_state.chart = TimeSeriesChart.plot_prediction_chart(
            old_data, predictions, upper, lower
        )
    except ValueError as e:
        error_modal(e)


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
        st.write("You should water your plant in:")
        st.write(st.session_state.prediction)
    st.write("## Prediction Graph")
    if st.session_state.show_chart:
        st.plotly_chart(st.session_state.chart)
    st.write(
        "Disclaimer: The model is trained on Chlorophytum bichetii (Karrer) Backer plant (เศรษฐีเรือนนอก)."
    )
    st.write("The sample plant is in an indoor environment, with constant airflow.")
