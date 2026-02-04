from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

import bot.core.keyboards as keyboards_core
from bot.apps.sendmessage import keyboards as keyboards_sendmessage
from bot.apps.sendmessage.state_fms import *

from bot.database.repository import UserRepository

router = Router()


@router.message(F.text)
async def sendmessage(message: Message, session: AsyncSession):
    repo = UserRepository(session)
    if message.message_thread_id:
        telegram_id = await repo.get_telegram_id_by_topic_id(message.message_thread_id)
        await message.bot.send_message(chat_id=telegram_id, text=message.text)
        return
    print(message.from_user.id)
    topic_id = await repo.get_topic_id_by_telegram_id(message.from_user.id)
    await message.bot.send_message(
            chat_id=-1003878748753,
            message_thread_id=topic_id,
            text=f"👤 {message.from_user.full_name}:\n\n{message.text}"
        )


    
    