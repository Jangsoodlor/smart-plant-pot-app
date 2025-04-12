import json
from io import StringIO

import pandas as pd
import requests
import streamlit as st


class APIFetcher:
    URL = "http://localhost:8080/moisture/v1"

    @classmethod
    @st.cache_data
    def aggregate_data(
        cls, source: str, frequency: int = 3, data_range: int = 3
    ) -> pd.DataFrame:
        url = f"{cls.URL}/{source}/aggregate?days={data_range}&hours={frequency}"
        response = requests.get(url)
        return pd.read_json(StringIO(response.text))

    @classmethod
    def get_latest_data(cls, source: str) -> dict:
        url = f"{cls.URL}/{source}/latest"
        response = requests.get(url)
        return json.loads(response.text)

    @classmethod
    def get_attributes(cls, source: str) -> list[str]:
        return [key for key in cls.get_latest_data(source).keys()]
