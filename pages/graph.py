import streamlit as st
import pandas as pd
import requests
import plotly.express as px


@st.cache_data
def get_dataframe():
    url = "http://localhost:8080/moisture/v1/sensor/aggregateHour/3"
    f = requests.get(url)
    return pd.read_json(f.text)

st.write("# Average Moisture every 3 hours")

df = get_dataframe()
# st.line_chart(x='readTime', y='soilMoisture', data=df)
fig = px.line(x=df['readTime'], y=df['soilMoisture'])
st.plotly_chart(fig)

