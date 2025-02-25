import httpx
from dataclasses import dataclass

from src.weather.wheather_fetcher_interface import WheatherFetcher
from src.weather.wheather_report_model import WeatherData, WeatherReport


@dataclass
class GeoData:
    country: str
    placename: str
    lat: str
    lng: str


class GeoNamesOpenMeteoFetcher(WheatherFetcher):
    def __init__(self, geonames_token: str):
        self.geonames_token = geonames_token
        self.client = httpx.AsyncClient()
    
    
    async def get_weather_report(self, placename: str):
        geodata = await self._get_geodata(placename)
        lat, lng = geodata.lat, geodata.lng
        
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
        response = await self.client.get(api_url)
        data = response.json()["current"]
        
        weather_data = WeatherData(
            country=geodata.country,
            placename=geodata.placename,
            temperature=data["temperature_2m"],
            humidity=data["relative_humidity_2m"],
            cloud_cover=data["cloud_cover"],
            wind_speed=data["wind_speed_10m"],
            wind_direction=data["wind_direction_10m"],
            wind_gusts=data["wind_gusts_10m"],
            precipitation=data["precipitation"],
            is_day=data["is_day"]
        )
        wheather_report = WeatherReport(weather_data)
        
        return wheather_report
    
    
    async def _get_geodata(self, placename: str):
        api_url = f"https://secure.geonames.org/searchJSON?q={placename}&maxRows=1&username={self.geonames_token}"
        response = await self.client.get(api_url)
        res = response.json()["geonames"][0]
        geodata = GeoData(res["countryName"], res["name"], res["lat"], res["lng"],)
        
        return geodata