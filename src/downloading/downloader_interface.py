from abc import ABC, abstractmethod
from src.downloading.track_model import Track


class Downloader(ABC):
    @abstractmethod
    async def download_youtube_track(self, url: str) -> Track:
        raise NotImplementedError

    
    @abstractmethod
    async def download_soundcloud_track(self, url: str) -> Track:
        raise NotImplementedError