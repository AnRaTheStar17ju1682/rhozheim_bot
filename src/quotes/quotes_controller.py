import io

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile

from src.dependencies import Dependencies

from src.quotes.quote_model import Quote
from PIL import Image


router = Router()


@router.message(Command("quote"))
async def quote_message(message: Message, bot: Bot, deps: Dependencies):
    if message.reply_to_message:
        original_message = message.reply_to_message
        is_anonym = False
        
        if getattr(original_message, "forward_from"):
            user_id = original_message.forward_from.id
            full_name = original_message.forward_from.full_name
        elif original_message.forward_sender_name:
            is_anonym = True
            full_name = original_message.forward_sender_name
        else:
            user_id = original_message.from_user.id
            full_name = original_message.from_user.full_name
            
        if not is_anonym:
            photos = await bot.get_user_profile_photos(user_id, limit=1)
            
            if photos.photos:
                buffer = io.BytesIO()
                photo_file_id = photos.photos[0][-1].file_id
                file = await bot.get_file(photo_file_id)
                await message.bot.download(file, destination=buffer)
                
                avatar = Image.open(buffer)
            else:
                avatar = None
        else:
            avatar = None
        
        q = Quote(
            text = original_message.text,
            name = full_name,
            avatar=avatar,
            name_color=(0, 0, 255) if is_anonym else get_color(user_id)
        )
        
        await message.reply_sticker(BufferedInputFile(q.quote_image.getvalue(), "randomsticker54622234"))
    else:
        await message.reply("Please reply to a message to quote it 🤓")


def get_color(id: int) -> tuple:
    return {
        0: (255, 0, 0),  # красный
        1: (255, 165, 0),  # оранжевый
        2: (128, 0, 128),  # фиолетовый
        3: (0, 128, 0),  # зелёный
        4: (173, 216, 230),  # голубой
        5: (0, 0, 255),  # синий
        6: (255, 192, 203)  # розовый
    }[abs(id) % 7]