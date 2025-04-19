import connexion
import six

from swagger_server.models.sensor_data import SensorData  # noqa: E501
from swagger_server.models.weather_data import WeatherData  # noqa: E501
from swagger_server import util


def controller_aggregate_sensor_data(days=None, hours=None):  # noqa: E501
    """Returns a list of average sensor readings of every user-specified interval for the last user-specified days.

     # noqa: E501

    :param days: 
    :type days: int
    :param hours: 
    :type hours: int

    :rtype: List[SensorData]
    """
    return 'do some magic!'


def controller_aggregate_weather_data(days=None, hours=None):  # noqa: E501
    """Returns a list of average sensor readings of every user-specified interval for the last user-specified days.

     # noqa: E501

    :param days: 
    :type days: int
    :param hours: 
    :type hours: int

    :rtype: List[WeatherData]
    """
    return 'do some magic!'


def controller_get_latest_sensor_data():  # noqa: E501
    """Returns the latest sensor readings (light, temperature, soil moisture).

     # noqa: E501


    :rtype: SensorData
    """
    return 'do some magic!'


def controller_get_latest_weather_data():  # noqa: E501
    """Returns the latest weather data from open-meteo

     # noqa: E501


    :rtype: WeatherData
    """
    return 'do some magic!'
