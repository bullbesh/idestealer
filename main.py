import logging
import os

import aiogram
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import sqlite3


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
async def add_id(message):
    connect = sqlite3.connect("users.db")
    cursor = connect.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS login_id(
		id INTEGER
	)"""
    )

    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()

    if data is None:
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
        connect.commit()

        await message.answer("Ваше id успешно добавлено!")
    else:
        await message.answer("Такое id уже существует!")


@dp.message_handler(commands=["delete"])
async def delete_id(message):
    connect = sqlite3.connect("users.db")
    cursor = connect.cursor()

    people_id = message.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
    connect.commit()

    await message.answer("Ваше id успешно удалено!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
