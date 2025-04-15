import datetime
import unittest


def str_to_time_obj(iso: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self._url = "http://localhost:8080/moisture/v1/"

    def assert_correct_sensor_schema(self, data: dict):
        self.assertIn("readTime", data)
        self.assertIn("temperature", data)
        self.assertIn("soilMoisture", data)
        self.assertIn("light", data)

    def assert_correct_weather_schema(self, data: dict):
        self.assertIn("readTime", data)
        self.assertIn("apiTemperature", data)
        self.assertIn("humidity", data)
        self.assertIn("cloudCover", data)
        self.assertIn("precipitation", data)

    def assert_frequency_diff(self, data: list[dict], hrs: int):
        freq_diff = str_to_time_obj(data[-1]["readTime"]) - str_to_time_obj(
            data[-2]["readTime"]
        )
        print(freq_diff)
        self.assertEqual(freq_diff.seconds, hrs * 60**2)

    def assert_range_diff(self, data: list[dict], days: int):
        range_diff = str_to_time_obj(data[-1]["readTime"]) - str_to_time_obj(
            data[0]["readTime"]
        )
        self.assertEqual(range_diff.days, days)
