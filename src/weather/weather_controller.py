from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from src.dependencies import Dependencies


router = Router()


@router.message(Command("weather"))
async def voice_handler(message: Message, bot: Bot, deps: Dependencies):
    placename = message.text[9:] 
    report = await deps.wheather_fetcher.get_weather_report(placename)
    
    await message.reply(report.generate_message())