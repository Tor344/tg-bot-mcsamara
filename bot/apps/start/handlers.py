from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

import bot.core.keyboards as keyboards_core
from bot.apps.start import keyboards as keyboards_satart
from bot.apps.start.state_fms import *

from bot.database.repository import UserRepository


router = Router()


@router.message(Command("start"))
async def start(message: Message, session: AsyncSession):
    repo = UserRepository(session)

    user = await repo.get_by_telegram_id(message.from_user.id)
    if not user:
        await repo.create(message.from_user.id)
        try:
            # Создаем топик
            result = await message.bot.create_forum_topic(
                chat_id=-1003878748753,
                name=f"@{message.from_user.username}, {message.from_user.id}"
            )
            
            await message.answer(f"Топик создан! ID: {result.message_thread_id}\n"
                                  f"Имя пользователя:{message.from_user.username}\n"
                                  f"Id пользователя:{message.from_user.id}")
        
        except BaseException as e: 
            pass

    await message.answer("start")

