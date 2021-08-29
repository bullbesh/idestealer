import logging
import os

import sqlite3

import aiogram
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import sql


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def send_welcome(message):
    """Send a greeting with a short description of the bot."""
    await message.answer(
        "Бот с базой данных, содержащих в себе id пользователей.\n\n"
        "/add - добавить своё id\n"
        "/delete - удалить своё id из базы",
    )


@dp.message_handler(commands=["add"])
async def send_add_id(message):
    people_id = message.chat.id
    user_id = [people_id]

    sql.add_id(people_id, user_id)

    await message.answer("Ваше id успешно добавлено!")


@dp.message_handler(commands=["delete"])
async def send_delete_id(message):
    people_id = message.chat.id

    sql.delete_id(people_id)

    await message.answer("Ваше id успешно удалено!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
