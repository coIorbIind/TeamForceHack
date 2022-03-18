from aiogram import types
from aiogram.dispatcher import Dispatcher


async def echo_command(message: types.Message) -> None:
    # print(message.from_user.id)
    await message.answer("Команда не распознана")


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(echo_command)
