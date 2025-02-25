from pydantic import BaseModel

from src.voice_recognizing.voice_recognzer_interface import VoiceRecognizer
from src.downloading.downloader_interface import Downloader 
from src.weather.wheather_fetcher_interface import WheatherFetcher


class Dependencies(BaseModel):
    voice_recognizer: VoiceRecognizer
    downloader: Downloader
    wheather_fetcher: WheatherFetcher
    
    class Config:
        arbitrary_types_allowed = True