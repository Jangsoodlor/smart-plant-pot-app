import streamlit as st
from APIFetcher import APIFetcher

if __name__ == "__main__":
    st.write("# Current sensor readings")
    st.write(APIFetcher.get_latest_data("sensor"))
    st.write("# Current weather")
    st.write(APIFetcher.get_latest_data("weather"))