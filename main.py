from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os
from sys import exit


from handlers import other, client
from config import load_config, BotConfig


async def on_startup(_) -> None:
    """
    A function that fires when the bot starts
    """
    # admins_ids = os.getenv("ADMINS_IDS").split()
    # for admin_id in admins_ids:
    #     await bot.send_message(chat_id=admin_id, text="Бот запущен")
    print("Success")


def main():
    """
    A bot, dispatcher, and data store object is created.
    Registering user input handlers.
    Running long polling
    """
    # Создание хранилища данных
    storage = MemoryStorage()
    # Создание бота
    # bot_token = os.getenv("TOKEN")
    # if not bot_token:
    #     exit("[ERROR] No token provided")
    bot_config_instance = load_config("config.cfg", "=")
    if bot_config_instance is None:
        exit("[ERROR] No token provided")

    bot = Bot(token=bot_config_instance.bot_token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)


    # Регистрания handlers
    # client.register_client_handlers(dp, bot)
    # exceptions.register_exceptions_handler(dp)
    client.register_admin_handlers(dp)
    other.register_other_handlers(dp)

    # Запуск поллинга
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)


if __name__ == "__main__":
    main()
