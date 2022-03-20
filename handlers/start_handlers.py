from aiogram.dispatcher import Dispatcher
from aiogram import types
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


def register_start_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_command, commands=['start'])
