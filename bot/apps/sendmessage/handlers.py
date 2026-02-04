import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import FSInputFile
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


@router.message(F.document)
async def sendmessage(message: Message, session: AsyncSession):
    try:
        repo = UserRepository(session)
        caption = message.caption if message.caption != None else "" 
        file_name = message.document.file_name
        file_id = message.document.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        await message.bot.download_file(file_path, "download/" + file_name)
        document = FSInputFile("download/" + file_name)

        if message.message_thread_id:
            telegram_id = await repo.get_telegram_id_by_topic_id(message.message_thread_id)
            await message.bot.send_document(chat_id=telegram_id, document=document, caption=caption)
            return
        print(message.from_user.id)
        topic_id = await repo.get_topic_id_by_telegram_id(message.from_user.id)
        await message.bot.send_document(
                chat_id=-1003878748753,
                message_thread_id=topic_id,
                document=document,
                caption=f"👤 {message.from_user.full_name}:\n\n{caption}")

    except BaseException as e:
        print(e)

    finally:
        print("download/" + file_name)
        os.remove("download/" + file_name)
