# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.sensor_data import SensorData  # noqa: E501
from swagger_server.models.weather_data import WeatherData  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_controller_aggregate_sensor_data(self):
        """Test case for controller_aggregate_sensor_data

        Returns a list of average sensor readings of every user-specified interval for the last user-specified days.
        """
        query_string = [('days', 56),
                        ('hours', 56)]
        response = self.client.open(
            '/sensor/aggregate',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_aggregate_weather_data(self):
        """Test case for controller_aggregate_weather_data

        Returns a list of average sensor readings of every user-specified interval for the last user-specified days.
        """
        query_string = [('days', 56),
                        ('hours', 56)]
        response = self.client.open(
            '/weather/aggregate',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_latest_sensor_data(self):
        """Test case for controller_get_latest_sensor_data

        Returns the latest sensor readings (light, temperature, soil moisture).
        """
        response = self.client.open(
            '/sensor/latest',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_latest_weather_data(self):
        """Test case for controller_get_latest_weather_data

        Returns the latest weather data from open-meteo
        """
        response = self.client.open(
            '/weather/latest',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
