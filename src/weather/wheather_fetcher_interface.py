from abc import ABC, abstractmethod

from src.weather.wheather_report_model import WeatherReport


class WheatherFetcher(ABC):
    @abstractmethod
    async def get_weather_report(self, placename: str) -> WeatherReport:
        raise NotImplementedError