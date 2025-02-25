from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.downloading.downloader_controller import router as d_router
from src.quotes.quotes_controller import router as q_router
from src.voice_recognizing.voice_recognizer_controller import router as v_router
from src.weather.weather_controller import router as w_router


main_router = Router()
main_router.include_routers(d_router, q_router, v_router, w_router)


@main_router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        f"""Hello, {html.bold(message.from_user.full_name)}!\n
i'm Rhozheim bot 😎.\n
What can i do?
1. Download music from soundcloud and youtube 🎧 (/pullmusic (url))
2. Translate voice to text 🗣 -> 💬
3. Tell you current weather in any region 👺👺👺 (/weather (placename))
4. Save messages as quotes to chat stickerpack 🤯🤯 (/quote to create a quote first)"""
    )