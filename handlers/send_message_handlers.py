from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import types, Bot
from keyboards.keyboards import main_keyboard
from .state_machine import SendMessageToTopic
from database.DataBaseRunner import DataBaseRunner


db_runner = DataBaseRunner()
global_bot: Bot = None


async def enter_topic(message: types.Message, state: FSMContext) -> None:
    """
    Enter name of new topic
    :param message: message containing the title of the topic
    :param state: form state
    """
    topic = db_runner.get_topic_by_name(message.text)
    if topic is None:
        await message.answer("Такой темы не существует, попробуйте снова")
        return

    async with state.proxy() as data:
        data['topic_name'] = topic.name

    await SendMessageToTopic.next()
    await message.answer("Введите содержание письма")


async def enter_message(message: types.Message, state: FSMContext) -> None:
    """
    Enter message for distribution
    :param message: message containing the mailing text
    :param state: form state
    """
    async with state.proxy() as data:
        data['message'] = message.text
        topic = topic = db_runner.get_topic_by_name(data["topic_name"])
        author_id = topic.author.chat_id

        msg = f"Новое сообщение по теме #{topic.name}\n\n@{message.from_user.username}: {message.text}"
        db_runner.add_message(message.text, topic.name, message.from_user.username)

        await message.answer("Сообщение отправлено", reply_markup=main_keyboard())
        await global_bot.send_message(chat_id=author_id, text=msg)

    await state.finish()


def register_send_message_handlers(dp: Dispatcher, bot: Bot) -> None:
    global global_bot
    global_bot = bot
    dp.register_message_handler(enter_topic, state=SendMessageToTopic.enter_topic)
    dp.register_message_handler(enter_message, state=SendMessageToTopic.enter_message)


