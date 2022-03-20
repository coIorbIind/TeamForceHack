from aiogram.dispatcher import Dispatcher
from aiogram import types

from handlers.show_topics_handlers import show_topics
from handlers.state_machine import AppStates, SendMessageToTopic
from keyboards.keyboards import main_keyboard
from database.DataBaseRunner import DataBaseRunner

db_runner = DataBaseRunner()


async def start_command(message: types.Message) -> None:
    """
    Welcome
    :param message: start message
    """
    db_runner.create_user(username=message.from_user.username, chat_id=message.from_user.id)
    await message.answer("Добро пожаловать в бота-менеджера", reply_markup=main_keyboard())


async def go_to_show_topics(message: types.Message) -> None:
    await AppStates.showing_topics.set()
    await show_topics(message, AppStates.showing_topics)


async def go_to_send_message(message: types.Message) -> None:
    await SendMessageToTopic.enter_topic.set()
    await message.answer("Для выхода из режима заполнения топика введите команду /cancel")
    await message.answer("Введите название топика", reply_markup=types.ReplyKeyboardRemove())


def register_start_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(go_to_show_topics,
                                lambda message: message.text == "Просмотреть все свои темы")
    dp.register_message_handler(go_to_send_message, lambda message: message.text == "Написать сообщение в тему")
