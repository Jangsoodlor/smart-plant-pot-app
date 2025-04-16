import datetime
import unittest


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
        self.assertIn("temperature", data)
        self.assertIn("humidity", data)
        self.assertIn("cloudCover", data)
        self.assertIn("precipitation", data)

    def assert_frequency_diff(self, data: list[dict], hrs: int):
        freq_diff = self.str_to_time_obj(data[-1]["readTime"]) - self.str_to_time_obj(
            data[-2]["readTime"]
        )
        print(freq_diff)
        self.assertEqual(freq_diff.seconds, hrs * 60**2)

    def str_to_time_obj(self, iso: str) -> datetime.datetime:
        return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))

    def assert_range_diff(self, data: list[dict], days: int):
        time1 = self.str_to_time_obj(data[0]["readTime"])
        time2 = self.str_to_time_obj(data[-1]["readTime"])
        range_diff_hours = (time2 - time1).total_seconds() / 3600
        self.assertGreater(range_diff_hours, (days - 1) * 24)
