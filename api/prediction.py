from datetime import datetime, timedelta

import numpy as np
import pandas as pd


class PredictMoisture:
    """Get prediction of soil moisture"""

    __instance = None

    def __init__(self):
        self.__model = None # MAY NOT BE NECESSARY
        self.__prediction_cache: pd.DataFrame | None = None
        # self.__model = load model from .pkl file

    def __new__(cls):
        """Singleton __new__ constructor"""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def set_model(self, model):
        """(MAY NOT BE NECESSARY) Update the data used to predict soil moisture

        :param data: Any data (idk what this would look like.
        Basically we use the same query as in creating sarimax table in
        controller.py and throw the result here and make it a dataframe somehow)
        """
        self.__model = model
        return self

    def predict_duration(self, moisture_amount: float | int) -> str:
        """Get the duration until the plant needs to be watered again
        based on moisture_amount.

        :param moisture_amount: desired level of soil moisture
        :return: A string representing the duration from now
        until the plant needs to be watered.
        """
        # Here we do for loop in self.__prediction_cache until finding the day where
        # moisture_amount > predicted_moisture_amount
        # DON'T NEED TO UPDATE self.__prediction_cahce, since in controller
        # self.get_prediction get called first.
        return "3000 days"

    def get_predictions(self) -> pd.DataFrame:
        """Get the predictions of soil moisture up to 7 days ahead.

        :return: A pandas dataframe consisting of ts (time)
        and soil_moisture (float) columns.
        """
        # In the final implementation this is where we do the model logic
        # something like:
        # model.fit(self.__df).predict() or something (idk the syntax)
        self.__prediction_cache = self.__get_dummy_data()
        return self.__prediction_cache

    def __get_dummy_data(self) -> pd.DataFrame:
        """Get dummy data predictions data. Will be removed after the code is done."""
        timestamps = [datetime.now() - timedelta(hours=i) for i in range(100)][::-1]

        moisture_values = np.random.uniform(low=10.0, high=60.0, size=100)

        df = pd.DataFrame({"ts": timestamps, "soil_moisture": moisture_values})
        return df
