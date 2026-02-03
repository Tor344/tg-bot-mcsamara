from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

import bot.core.keyboards as keyboards_core
from bot.apps.sendmessage import keyboards as keyboards_sendmessage
from bot.apps.sendmessage.state_fms import *

from bot.database.repository import UserRepository

router = Router()


@router.message()
async def sendmessage(message: Message, session: AsyncSession):
    repo = UserRepository(session)

    await message.answer("sendmessage")
    