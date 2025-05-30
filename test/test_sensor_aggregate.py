import json

import requests
from base_test_case import BaseTestCase


class TestAggregateSensor(BaseTestCase):
    def test_aggregate_without_query_params(self):
        response = requests.get(self._url + "sensor/aggregate")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data, list)
        self.assert_correct_sensor_schema(data[-1])
        self.assert_frequency_diff(data, 3)
        self.assert_range_diff(data, 3)

    def test_aggregate_with_valid_hours_param(self):
        for i in (1, 2):
            response = requests.get(self._url + f"sensor/aggregate?hours={i}")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.text)
            self.assertIsInstance(data, list)
            self.assert_correct_sensor_schema(data[-1])
            self.assert_frequency_diff(data, i)
            self.assert_range_diff(data, 3)

    def test_aggregate_with_valid_days_param(self):
        for i in (1, 2):
            response = requests.get(self._url + f"sensor/aggregate?days={i}")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.text)
            self.assertIsInstance(data, list)
            self.assert_correct_sensor_schema(data[-1])
            self.assert_frequency_diff(data, 3)
            self.assert_range_diff(data, i)

    def test_aggregate_with_hours_and_days_param(self):
        response = requests.get(self._url + "sensor/aggregate?days=2&hours=2")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data, list)
        self.assert_correct_sensor_schema(data[-1])
        self.assert_frequency_diff(data, 2)
        self.assert_range_diff(data, 2)

    def test_aggregate_with_non_int_hours_param(self):
        response = requests.get(self._url + "sensor/aggregate?hours=0.5")
        self.assertEqual(response.status_code, 400)

    def test_aggregate_with_invalid_int_hours_param(self):
        response = requests.get(self._url + "sensor/aggregate?hours=5")
        self.assertEqual(response.status_code, 400)

    def test_aggregate_with_non_positive_hours_param(self):
        for i in (-1, 0):
            response = requests.get(self._url + f"sensor/aggregate?hours={i}")
            self.assertEqual(response.status_code, 400)

    def test_aggregate_with_non_int_days_hours_param(self):
        response = requests.get(self._url + "sensor/aggregate?days=0.5")
        self.assertEqual(response.status_code, 400)

    def test_aggregate_with_non_positive_days_param(self):
        for i in (-1, 0):
            response = requests.get(self._url + f"sensor/aggregate?days={i}")
            self.assertEqual(response.status_code, 400)
