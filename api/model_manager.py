import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime


class ModelManager:
    __instance = None

    @classmethod
    def get_model(cls):
        return cls.__instance

    @classmethod
    def set_model(cls, instance):
        cls.__instance = instance


class ModelBuilder:
    def __init__(self):
        self.main_data = None
        self.exog_models = []
        self.exog_columns = []
        self.predicting_column = None
        self.exog_training_values = None
        self.exog_predicting_values = None
        self.order = None
        self.model = None
        self.timedelta = None

    def add_exog(
        self,
        column_name: str,
        order: tuple[int, int, int],
        seasonal_order: tuple[int, int, int, int],
    ):
        self.exog_columns.append(column_name)
        model = SARIMAX(
            endog=self.main_data[column_name],
            order=order,
            seasonal_order=seasonal_order,
        )
        self.exog_models.append({"name": column_name, "model": model.fit()})
        return self

    def add_basic_init(
        self,
        dataframe: pd.DataFrame,
        predicting_column: str,
        order: tuple[int, int, int],
        time_delta: pd.Timedelta,
    ):
        self.main_data = dataframe
        self.predicting_column = predicting_column
        self.order = order
        self.timedelta = time_delta
        return self

    def build(self):
        model = Model(self)
        ModelManager.set_model(model)
        return model


class Model:
    def __init__(self, builder: ModelBuilder):
        """
        Init the model
        :param dataframe: The dataframe containing all the columns
        :param predicting_column: The name of the predicting column
        :param exog_columns: The list of exog columns.
        :param order: The order of ARIMAX model
        """
        self.main_data = builder.main_data
        self.__predicting_column = builder.predicting_column
        self.__exog_models = builder.exog_models
        self.__exog_columns = builder.exog_columns
        self.__exog_training_values = builder.exog_training_values
        self.__exog_predicting_values = builder.exog_predicting_values
        self.__order = builder.order
        self.__model = builder.model
        self.__timedelta = builder.timedelta
        self.__cached_prediction = {}

    def __get_exog_data(self, steps: int):
        for model in self.__exog_models:
            predicted = model["model"].get_forecast(steps=steps).predicted_mean
            predicted.columns = [model["name"]]
            if self.__exog_predicting_values is None:
                self.__exog_predicting_values = predicted
            else:
                self.__exog_predicting_values = pd.concat(
                    [self.__exog_predicting_values, predicted], axis=1
                )

    def fit_model(self):
        if self.__exog_columns[0] is None:
            model = SARIMAX(
                endog=self.main_data[self.__predicting_column], order=self.__order
            )
        else:
            model = SARIMAX(
                endog=self.main_data[self.__predicting_column],
                exog=self.main_data[self.__exog_columns],
                order=self.__order,
            )
        self.__model = model.fit()
        return self

    def get_prediction(self, steps: int):
        try:
            cached_duration = (datetime.now() - self.__cached_prediction["ts"]).days
            if cached_duration > 1:
                self.__cached_prediction = {}
                raise ValueError("Please update dataframe")
            if len(self.__cached_prediction) == 4 and cached_duration < 1:
                return (
                    self.__cached_prediction["predicted"],
                    self.__cached_prediction["upper"],
                    self.__cached_prediction["lower"],
                )
        except KeyError:
            pass

        if self.__model is None:
            raise AttributeError("The model is not fitted yet")
        self.__get_exog_data(steps)
        predicted_obj = self.__model.get_forecast(
            steps=steps, exog=self.__exog_predicting_values
        )
        predicted = predicted_obj.predicted_mean
        forecast_index = pd.date_range(
            start=self.main_data.index[-1] + self.__timedelta,
            freq=self.__timedelta,
            periods=steps,
        )
        predicted.columns = ["predicted"]
        predicted.index = forecast_index
        forecast_ci = predicted_obj.conf_int()
        lower = forecast_ci.iloc[:, 0]
        lower.index = forecast_index
        upper = forecast_ci.iloc[:, 1]
        upper.index = forecast_index
        self.__cached_prediction["predicted"] = predicted
        self.__cached_prediction["upper"] = upper
        self.__cached_prediction["lower"] = lower
        self.__cached_prediction["ts"] = datetime.now()

        return predicted, upper, lower

    def get_duration(self, moisture_level: int) -> str:
        """
        Returns the duration of days (from the last day in the training data)
        that the moisture will be at the specified level.
        The maximum date is 7 days.

        :param moisture_level: The integer of the moisture level you want.
        :return: The string of the number of days.
        """
        MAX_DAY = 7
        AMOUNT_OF_POINTS_IN_A_DAY = (60 / 15) * 24
        predicted, upper, lower = self.get_prediction(
            AMOUNT_OF_POINTS_IN_A_DAY * MAX_DAY
        )
        matches = predicted[predicted <= moisture_level]
        if matches.empty:
            return f"More than {MAX_DAY} days"
        index = matches.index[0]
        number_of_days = (index - self.main_data.index[-1]).days
        return f"{number_of_days} " + (
            "day" if number_of_days == 1 or number_of_days == 0 else "days"
        )

    @property
    def df(self):
        return self.main_data
