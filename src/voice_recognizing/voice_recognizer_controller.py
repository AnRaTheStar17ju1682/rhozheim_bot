import io
import time

from aiogram import Bot, Router
from aiogram.types import Message

from src.dependencies import Dependencies


router = Router()


@router.message(lambda message: message.voice)
async def voice_handler(message: Message, bot: Bot, deps: Dependencies):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    buffer = io.BytesIO()
    await message.bot.download(file, destination=buffer)
    
    msg = await message.reply("🔍 Распознаю речь...")
    
    start = time.time()
    async for text in deps.voice_recognizer.recognize_speech(buffer):
        now = time.time()
        
        if (now - start) > 1:
            await msg.edit_text(f"🔍 Распознаю речь: {text}...")
            start = time.time()  
        else:
            continue
    
    await msg.edit_text(f"{text}")