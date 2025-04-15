import json

import requests
from base_test_case import BaseTestCase


class TestAggregateWeather(BaseTestCase):
    def test_aggregate_without_query_params(self):
        response = requests.get(self._url + "weather/aggregate")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data, list)
        self.assert_correct_weather_schema(data[-1])
        self.assert_frequency_diff(data, 3)
        self.assert_range_diff(data, 3)

    def test_aggregate_with_hours_param(self):
        response = requests.get(self._url + "weather/aggregate?hours=2")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data, list)
        self.assert_correct_weather_schema(data[-1])
        self.assert_frequency_diff(data, 2)
        self.assert_range_diff(data, 3)

    def test_aggregate_with_days_param(self):
        response = requests.get(self._url + "weather/aggregate?days=2")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data, list)
        self.assert_correct_weather_schema(data[-1])
        self.assert_frequency_diff(data, 3)
        self.assert_range_diff(data, 2)

    def test_aggregate_with_hours_and_days_param(self):
        response = requests.get(self._url + "weather/aggregate?days=2&hours=2")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data, list)
        self.assert_correct_weather_schema(data[-1])
        self.assert_frequency_diff(data, 2)
        self.assert_range_diff(data, 2)

    def test_aggregate_with_non_int_hours_param(self):
        response = requests.get(self._url + "weather/aggregate?hours=0.5")
        self.assertEqual(response.status_code, 400)

    def test_aggregate_with_invalid_int_hours_param(self):
        response = requests.get(self._url + "weather/aggregate?hours=5")
        self.assertEqual(response.status_code, 400)

    def test_aggregate_with_invalid_days_hours_param(self):
        response = requests.get(self._url + "weather/aggregate?days=0.5")
        self.assertEqual(response.status_code, 400)
