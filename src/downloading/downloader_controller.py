import re

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile

from src.dependencies import Dependencies
from src.downloading.downloading_exeptions import PlaylistNotAllowedError


router = Router()


@router.message(Command("pullmusic"))
async def download_track(message: Message, bot: Bot, deps: Dependencies):
    text = message.text
    
    try:
        if yt_match := re.search(r"(?:(youtube.com|youtu.be)(\/watch\?v=)|(youtu.be\/))([^ ]{11})", text):
            url = "https://" + yt_match.group(0)
            track = await deps.downloader.download_youtube_track(url)
        elif sd_match := re.search(r"(?:(soundcloud\.com)(\/[^\s\/]*)(\/(?!popular-tracks|sets|albums|reposts|tracks)[^\s?\/]*))|(?:(on\.soundcloud\.com)\/[^ \s]*)", text):
            url = "https://" + sd_match.group(0)
            track = await deps.downloader.download_soundcloud_track(url)
        else:
            msg = "Bro, i can't find a soundcloud/youtube link in your message 😰😰👺👺.\n\
Maybe you sent to me a playlist or an author, but i don't support playlists downloading 😤😤."
                
            await message.reply(msg)
            return
        
        await message.reply_audio(
            audio=BufferedInputFile(track.audio, track.title),
            thumbnail=BufferedInputFile(track.thumbnail, "thumbnail.jpeg"),
            title=track.title
        )
        await message.answer("Here your track bro 👆👆😎😎")
    except PlaylistNotAllowedError:
        await message.reply("I DO NOT support downloading from playlists!!! 🙄🙄😤😤")