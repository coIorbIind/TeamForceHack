from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import NetworkError
from handlers import create_topic_handlers, other, show_topics_handlers, start_handlers, send_message_handlers


from sys import exit


#from handlers import other, client
from config import load_config
from config_classes import BotConfig


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
    bot_config_instance = load_config("config.cfg", BotConfig, "=")
    if bot_config_instance is None:
        exit("[ERROR] No token provided")

    bot = Bot(token=bot_config_instance.bot_token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)


    # Регистрания handlers
    # client.register_client_handlers(dp, bot)
    # exceptions.register_exceptions_handler(dp)

    create_topic_handlers.register_create_handlers(dp, bot)
    show_topics_handlers.register_show_topics_handlers(dp, bot)
    start_handlers.register_start_handlers(dp)
    send_message_handlers.register_send_message_handlers(dp, bot)
    # client.register_admin_handlers(dp)
    other.register_other_handlers(dp)

    # Запуск поллинга
    try:
        executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

    except NetworkError:
        exit("[ERROR] No connection")


if __name__ == "__main__":
    main()
