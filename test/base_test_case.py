import datetime
import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self._url = "http://localhost:8080/moisture/v1/"

    def assert_correct_sensor_schema(self, data: dict):
        self.assertIn("read_time", data)
        self.assertIn("temperature", data)
        self.assertIn("soil_moisture", data)
        self.assertIn("light", data)

    def assert_correct_weather_schema(self, data: dict):
        self.assertIn("read_time", data)
        self.assertIn("temperature", data)
        self.assertIn("humidity", data)
        self.assertIn("cloud_cover", data)
        self.assertIn("precipitation", data)

    def assert_frequency_diff(self, data: list[dict], hrs: int):
        freq_diff = self.str_to_time_obj(data[-1]["read_time"]) - self.str_to_time_obj(
            data[-2]["read_time"]
        )
        print(freq_diff)
        self.assertEqual(freq_diff.seconds, hrs * 60**2)

    def str_to_time_obj(self, iso: str) -> datetime.datetime:
        return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))

    def assert_range_diff(self, data: list[dict], days: int):
        time1 = self.str_to_time_obj(data[0]["read_time"])
        time2 = self.str_to_time_obj(data[-1]["read_time"])
        range_diff_hours = (time2 - time1).total_seconds() / 3600
        self.assertGreater(range_diff_hours, (days - 1) * 24)
