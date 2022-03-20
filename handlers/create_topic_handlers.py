from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import types, Bot
from keyboards.keyboards import main_keyboard
from .state_machine import CreateTopic
from database.DataBaseRunner import DataBaseRunner


db_runner = DataBaseRunner()
global_bot: Bot = None


async def create_topic(message: types.Message) -> None:
    """
    Start creating a topic
    :param message: message from user
    """
    await CreateTopic.topic_name.set()
    await message.answer("Для выхода из режима заполнения топика введите команду /cancel")
    await message.answer("Введите название топика", reply_markup=types.ReplyKeyboardRemove())


async def enter_name(message: types.Message, state: FSMContext) -> None:
    """
    Enter name of new topic
    :param message: message containing the title of the topic
    :param state: form state
    """
    async with state.proxy() as data:
        data['topic_name'] = message.text
    await CreateTopic.next()
    await message.answer("Введите содержание письма")


async def enter_message(message: types.Message, state: FSMContext) -> None:
    """
    Enter message for distribution
    :param message: message containing the mailing text
    :param state: form state
    """
    async with state.proxy() as data:
        data['message'] = message.text
    await CreateTopic.next()
    await message.answer("Введите адресатов через \";\"")


async def enter_addressees(message: types.Message, state: FSMContext) -> None:
    """
    Enter message addressees
    :param message: message containing message addressees
    :param state: form state
    """
    async with state.proxy() as data:
        data['addressees'] = [item.strip() for item in message.text.split(";")]
        print(data)
        db_runner.create_topic(
            username=message.from_user.username,
            topic_name=data["topic_name"],
            addressees=data["addressees"],
            text=data["message"]
        )
        topic = db_runner.get_topic_by_name(data['topic_name'])

        targ_receivers = topic.addressees

        text = f"#{topic.name}\n\n{topic.text}"
        for receiver in targ_receivers:
            t_chat_id = receiver.chat_id

            await global_bot.send_message(chat_id=t_chat_id, text=text)
        # send message to addressees
    await message.answer("Тема добавлена", reply_markup=main_keyboard())
    await state.finish()


def register_create_handlers(dp: Dispatcher, bot: Bot) -> None:
    global global_bot
    global_bot = bot
    dp.register_message_handler(create_topic, lambda message: message.text == "Добавить тему")
    dp.register_message_handler(enter_name, state=CreateTopic.topic_name)
    dp.register_message_handler(enter_message, state=CreateTopic.message)
    dp.register_message_handler(enter_addressees, state=CreateTopic.addressees)
