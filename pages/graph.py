import streamlit as st
import pandas as pd
import requests
import plotly.express as px


@st.cache_data
def get_dataframe():
    url = "http://localhost:8080/moisture/v1/sensor/aggregateHour/3"
    f = requests.get(url)
    return pd.read_json(f.text)


df = get_dataframe()
# st.line_chart(x='readTime', y='soilMoisture', data=df)

st.sidebar.header("Select Attribute")
with st.sidebar:
    radio_btn = st.radio(
        options=[col for col in df.columns if col != "readTime"],
        label="Select Attirbute",
        label_visibility="collapsed",
    )


st.write(f"# Average {radio_btn} every 3 hours")
fig = px.line(x=df["readTime"], y=df[radio_btn])
st.plotly_chart(fig)
