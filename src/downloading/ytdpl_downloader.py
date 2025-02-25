import yt_dlp
from io import BytesIO
import os
import asyncio
import uuid


from src.downloading.downloader_interface import Downloader
from src.downloading.downloading_exeptions import PlaylistNotAllowedError
from src.downloading.track_model import Track


class YTDPLDownloader(Downloader):
    async def download_youtube_track(self, url):
        buffer = await asyncio.to_thread(self._download_youtube_track_sync, url)
        
        return buffer
    
    
    def _download_youtube_track_sync(self, url: str) -> Track:
        random_name = uuid.uuid4()
        ydl_opts = {
            'format': 'bestaudio/best',
            'fragment_retries': 3,
            'retries': 3,
            'ignoreerrors': 'only_download',
            'force_ipv4': True,
            'external_downloader': 'axel',
            'external_downloader_args': ['-n', '3'],
            'outtmpl': f'{random_name}.%(ext)s',
            'writethumbnail': True,
            'extractor_args': {
                'youtube': {'player_client': ['android']}
            },
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=True)
            
            audio_path = data['requested_downloads'][0]['filepath']
            thumbnail_path = f"{random_name}.webp"
            title = (data["title"])
            
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            with open (thumbnail_path, "rb") as f:
                thumbnail_bytes = f.read()
            os.remove(audio_path)
            os.remove(thumbnail_path)
            
            track = Track(title, audio_bytes, thumbnail_bytes)
        
        return track
    
    
    async def download_soundcloud_track(self, url):
        buffer = await asyncio.to_thread(self._download_soundcloud_track_sync, url)
        
        return buffer
    
    
    def _download_soundcloud_track_sync(self, url):
        random_name = uuid.uuid4()
        ydl_opts = {
            'playlist_items': '0',
            #'format': 'bestaudio/best',
            'format': 'hls_opus_0_0',
            'writethumbnail': True,
            'embed_metadata': True,
            'postprocessors': [
                #{
                #    'key': 'FFmpegExtractAudio',
                #    'preferredcodec': 'opus',
                #    'preferredquality': '320',
                #},
            #    {'key': 'EmbedThumbnail'},
                {'key': 'FFmpegMetadata'},
            ],
            'outtmpl': f'{random_name}.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=True)
            
            # if not the "track" key in data it is a playlist or an album
            if not "track" in data:
                raise PlaylistNotAllowedError
            else:
                audio_path = data['requested_downloads'][0]['filepath']
                thumbnail_path = f"{random_name}.jpg"
                title = (data["title"])
            
                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()
                with open (thumbnail_path, "rb") as f:
                    thumbnail_bytes = f.read()
                os.remove(audio_path)
                os.remove(thumbnail_path)
                
                track = Track(title, audio_bytes, thumbnail_bytes)
        
                return track