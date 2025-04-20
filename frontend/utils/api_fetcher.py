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
        """Get aggregated data based on the following parameters.

        :param source: source of the data.
        :param frequency: sample frequency of the data (hours), defaults to 3
        :param data_range: range of the data (days), defaults to 3
        :raises ValueError: when the status code is not 200 (aka. something went wrong).
        :return: A pandas dataframe of the aggregated data.
        """
        url = f"{cls.URL}/{source}/aggregate?days={data_range}&hours={frequency}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Invalid Request.")
        return pd.read_json(StringIO(response.text))

    @classmethod
    def get_latest_data(cls, source: str) -> dict:
        """Get the latest data from a specified source.

        :param source: source of the data.
        :raises ValueError: when the status code is not 200 (aka. something went wrong).
        :return: A pandas dataframe of the aggregated data.
        """
        url = f"{cls.URL}/{source}/latest"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Invalid Request.")
        return json.loads(response.text)

    @classmethod
    def get_attributes(cls, source: str) -> list[str]:
        """Get all attributes of a table."""
        return [key for key in cls.get_latest_data(source).keys()]

    @classmethod
    def get_soil_moisture_prediction(
        cls, moisture_amount: float | int
    ) -> tuple[str, pd.DataFrame]:
        """Get soil moisture prediction.

        :param moisture_amount: The lowest soil moisture amount tolerable by the user.
        :raises ValueError: when the status code is not 200 (aka. something went wrong).
        :return: (duration until next watering is required,
        a pandas dataframe of the prediction).
        """
        url = f"{cls.URL}/predictmoisture/{moisture_amount}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Invalid Request.")
        result = json.loads(response.text)
        duration = result["duration"]
        predictions = pd.DataFrame.from_dict(result["predictions"])
        return duration, predictions
