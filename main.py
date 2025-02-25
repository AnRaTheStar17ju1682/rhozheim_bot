import logging
import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.rhozheim_bot import main_router
from src.voice_recognizing.local_recognizer import LocalRecognizer
from src.downloading.ytdpl_downloader import YTDPLDownloader
from src.weather.geonames_openmeteo_fetcher import GeoNamesOpenMeteoFetcher
from src.dependencies import Dependencies
from src.config import settings


TOKEN = settings.TOKEN
MODEL_PATH = settings.MODEL_PATH
GEONAMES_TOKEN = settings.GEONAMES_TOKEN

deps = Dependencies(
    voice_recognizer=LocalRecognizer(MODEL_PATH),
    downloader=YTDPLDownloader(),
    wheather_fetcher=GeoNamesOpenMeteoFetcher(GEONAMES_TOKEN)
)
logger = logging.getLogger()
dp = Dispatcher(deps=deps)
dp.include_router(main_router)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())