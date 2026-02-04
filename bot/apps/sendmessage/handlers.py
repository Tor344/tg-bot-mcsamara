import os
import asyncio
import json
from aiogram import Router, F
from aiogram.types import Message, InputMediaPhoto,InputMediaVideo,InputMediaDocument
from aiogram.filters import Command
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict

import bot.core.keyboards as keyboards_core
from bot.apps.sendmessage import keyboards as keyboards_sendmessage
from bot.apps.sendmessage.state_fms import *

from bot.database.repository import UserRepository

router = Router()


import config.settings

@router.message(F.text)
async def sendmessage(message: Message, session: AsyncSession):
    repo = UserRepository(session)
    if message.message_thread_id:
        telegram_id = await repo.get_telegram_id_by_topic_id(message.message_thread_id)
        await message.bot.send_message(chat_id=telegram_id, text=message.text)
        return
    
    topic_id = await repo.get_topic_id_by_telegram_id(message.from_user.id)
    await message.bot.send_message(
            chat_id=config.settings.chat_id,
            message_thread_id=topic_id,
            text=f"{message.text}"
        )
    

media_groups = {}


async def send_group(group_id, bot):
    await asyncio.sleep(1.5)

    group = media_groups[group_id]

    if group["caption"]:
        group["media"][0].caption = group["caption"]

    await bot.send_media_group(
        chat_id=group["chat_id"],
        message_thread_id=group["topic_id"],
        media=group["media"]
    )

    del media_groups[group_id]


@router.message(F.media_group_id)
async def handle_media_group(message: Message, session: AsyncSession):
    repo = UserRepository(session)
    group_id = message.media_group_id

    if group_id not in media_groups:
        media_groups[group_id] = {
            "media": [],
            "chat_id": None,
            "topic_id": None,
            "caption": None,
            "task": None
        }

    group = media_groups[group_id]


    if message.message_thread_id:

        group["chat_id"] = await repo.get_telegram_id_by_topic_id(
            message.message_thread_id
        )
        group["topic_id"] = None
    else:
  
        group["chat_id"] = config.settings.chat_id
        group["topic_id"] = await repo.get_topic_id_by_telegram_id(
            message.from_user.id
        )


    if message.caption:
        group["caption"] = f"{message.caption}"


    if message.photo:
        group["media"].append(
            InputMediaPhoto(media=message.photo[-1].file_id)
        )

    if message.video:
        group["media"].append(
            InputMediaVideo(media=message.video.file_id)
        )

    if message.document:
        group["media"].append(
            InputMediaDocument(media=message.document.file_id)
        )

    if not group["task"]:
        group["task"] = asyncio.create_task(send_group(group_id, message.bot))


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
                chat_id=config.settings.chat_id,
                message_thread_id=topic_id,
                document=document,
                caption=f"👤 {message.from_user.full_name}:\n\n{caption}")

    except BaseException as e:
        print(e)

    finally:
        print("download/" + file_name)
        os.remove("download/" + file_name)



@router.message(F.video)
async def sendmessage(message: Message, session: AsyncSession):
    repo = UserRepository(session)
    print("hello")
    caption = message.caption if message.caption != None else "" 
    video = message.video
    file_id = video.file_id
    if message.message_thread_id:
        telegram_id = await repo.get_telegram_id_by_topic_id(message.message_thread_id)
        await message.bot.send_video(chat_id=telegram_id, video=file_id, caption=caption)
        return
    topic_id = await repo.get_topic_id_by_telegram_id(message.from_user.id)
    await message.bot.send_video(
            chat_id=config.settings.chat_id,
            message_thread_id=topic_id,
            video=file_id,
            caption=f"{caption}")
    

@router.message(F.photo)
async def sendmessage(message: Message, session: AsyncSession):
    repo = UserRepository(session)
    caption = message.caption if message.caption != None else "" 
    photo = message.photo[-1]
    file_id = photo.file_id
    if message.message_thread_id:
        telegram_id = await repo.get_telegram_id_by_topic_id(message.message_thread_id)
        await message.bot.send_photo(chat_id=telegram_id, photo=file_id, caption=caption)
        return
    topic_id = await repo.get_topic_id_by_telegram_id(message.from_user.id)
    await message.bot.send_photo(
            chat_id=config.settings.chat_id,
            message_thread_id=topic_id,
            photo=file_id,
            caption=f"{caption}")