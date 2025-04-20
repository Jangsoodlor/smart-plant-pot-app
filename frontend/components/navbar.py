import streamlit as st

def navbar() -> None:
    with st.sidebar:
        st.title("Menu")
        st.page_link('main.py', label="Home", icon="🏡")
        st.page_link('pages/graph.py', label="Visualisation", icon="📊")
        st.page_link('pages/prediction.py', label="Watering Prediction", icon="🌊")