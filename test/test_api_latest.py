import json

import requests
from base_test_case import BaseTestCase


class TestLatest(BaseTestCase):
    def test_latest_sensor_data(self):
        response = requests.get(self._url + "sensor/latest")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data, dict)
        self.assert_correct_sensor_schema(data)

    def test_latest_weather_data(self):
        response = requests.get(self._url + "weather/latest")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data, dict)
        self.assert_correct_weather_schema(data)
