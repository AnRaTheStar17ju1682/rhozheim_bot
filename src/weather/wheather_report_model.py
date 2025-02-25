from dataclasses import dataclass


@dataclass
class WeatherData:
    country: str
    placename: str
    
    temperature: int
    humidity: int
    cloud_cover: int
    wind_speed: int
    wind_direction: int
    wind_gusts: int
    precipitation: int
    is_day: bool


class WeatherReport:
    def __init__(self, data: WeatherData):
        self.data = data
        self.message = []
    
    
    def generate_message(self):
        self._format_location()
        self._format_time()
        self._format_temperature()
        self._format_humidity()
        self._format_cloud_cover()
        self._format_wind_speed()
        self._format_wind_direction()
        self._format_wind_gusts()
        self._format_precipitation()
        return "".join(self.message)


    def _format_location(self):
        self.message.append(f"📍 Location: {self.data.country} - {self.data.placename}\n")
    
    
    def _format_time(self):
        self.message.append(f"🕰️ Time: {"☀️ day" if self.data.is_day else "🌑 night... 💤"}\n")
    
    
    def _format_temperature(self):
        def temperature_emoji():            
            if t < 20: return "☃️"
            if t < 10: return "❄️"
            if t < 10: return "☁️"
            if t < 20: return "🌴"
            if t < 30: return "🔥"
            return "🌋"
        
        t = self.data.temperature
        emoji = temperature_emoji()
        self.message.append(f"🌡️ Temperature: {t}°C {emoji}\n")
    
    
    def _format_humidity(self):
        def humidity_emoji():
            if h <= 30: return "🏕️"
            if h > 30: return "💦"
            if h > 60: return "🐟"
            return "🐳"
        
        h = self.data.humidity
        emoji = humidity_emoji()
        self.message.append(f"💧 Humidity: {h}% {emoji}\n")
    
    
    def _format_cloud_cover(self):
        def cloud_cover_emoji():
            if cv < 20: return "🏞️"
            if cv < 50: return "🌤️"
            if cv < 80: return "☁️"
            return "🌥️"
            
        cv = self.data.cloud_cover
        emoji = cloud_cover_emoji()
        self.message.append(f"🌫️ Cloud Cover: {cv}% {emoji}\n")
    
    
    def _format_wind_speed(self):
        def wind_emoji():
            if ws < 5:return "💤"
            if ws < 15:return "💨"
            if ws < 30:return "🌬️"
            return "🌪️"
            
        ws = self.data.wind_speed
        emoji = wind_emoji()
        self.message.append(f"💨 Wind Speed: {ws} km/h {emoji}\n")
    
    
    def _format_wind_direction(self):
        def direction():
            directions = [
                (337.5, 22.5, "North", "⬇️"),
                (22.5, 67.5, "North-East", "↙️"),
                (67.5, 112.5, "East", "⬅️"),
                (112.5, 157.5, "South-East", "↖️"),
                (157.5, 202.5, "South", "⬆️"),
                (202.5, 247.5, "South-West", "↗️"),
                (247.5, 292.5, "West", "➡️"),
                (292.5, 337.5, "North-West", "↘️")
            ]
            
            for start, end, name, emoji in directions:
                if start > end:
                    if wd >= start or wd < end:
                        return f"{name} {emoji}"
                elif wd >= start and wd < end:
                    return f"{name} {emoji}"
            return "Unknown"
        
        wd = self.data.wind_direction
        direction = direction()
        self.message.append(f"🗺️ Wind Direction: {direction}\n")
    
    
    def _format_wind_gusts(self):
        self.message.append(f"🌪️ Wind Gusts: {self.data.wind_gusts} km/h\n")
    
    
    def _format_precipitation(self):
        def precipitation_emoji():
            if prc == 0: return "☀️"
            if prc < 5: return "🌂"
            if prc < 10: return "🌨️"
            return "⛈️"
        
        prc = self.data.precipitation
        emoji =precipitation_emoji()
        self.message.append(f"🌨️ Precipitation: {prc} mm {emoji}\n")