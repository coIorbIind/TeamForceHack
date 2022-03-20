from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import types, Bot
from keyboards.keyboards import topics_keyboard, topic_info_keyboard
from database.DataBaseRunner import DataBaseRunner, dbe
from .state_machine import ShowTopic

db_runner = DataBaseRunner()
global_dispatcher: Dispatcher = None
global_bot: Bot = None


async def show_topics(message: types.Message) -> None:
    """
    Function to view the list of topics
    :param message: message from user
    """
    topics = db_runner.get_topics(message.from_user.username)
    if topics is None:
        await message.answer("Вы ещё не создали ни одной темы")
    else:
        await ShowTopic.showing_topic.set()
        for topic in topics:
            global_dispatcher.register_message_handler(topic_info,
                                                       lambda msg: msg.text == topic.name,
                                                       state=ShowTopic.showing_topic)
        await message.answer("Список ваших статей", reply_markup=topics_keyboard([topic.name for topic in topics]))


async def topic_info(message: types.Message, state: FSMContext):
    receivers = ""

    topic = db_runner.get_topic_by_name(message.text)

    async with state.proxy() as data:
        data['topic'] = topic.name

    if topic is None:
        await message.answer("Тема не найдена")

    else:
        await ShowTopic.next()
        for user in topic.addressees:
            receivers += f"@{user.tgm_link}; "
        await message.answer(f"#{topic.name}\n\n{topic.text}\n\nКорреспонденты: {{{receivers}}}",
                             reply_markup=topic_info_keyboard())


# async def change
async def send_message(message: types.Message, state: FSMContext):
    if message.text == "Отправить сообщение":
        await ShowTopic.next()
        await message.answer("Введите текст сообщения для рассылки", reply_markup=types.ReplyKeyboardRemove())


async def enter_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(data)
        topic = db_runner.get_topic_by_name(data['topic'])

        targ_receivers = topic.addressees
        print(topic.addressees)

        text = f"#{topic.name}\n\n{message.text}"
        for receiver in targ_receivers:
            t_chat_id = receiver.chat_id
            await global_bot.send_message(chat_id=t_chat_id, text=text)


def register_show_topics_handlers(dp: Dispatcher, bot: Bot) -> None:
    global global_dispatcher
    global_dispatcher = dp
    global global_bot
    global_bot = bot
    dp.register_message_handler(show_topics, lambda message: message.text == "Просмотреть все свои темы")
    # dp.register_message_handler(lambda message: ShowTopic.send_message.set(),
    #                             lambda message: message.text == "Отправить сообщение")
    # dp.register_message_handler(send_message, state=ShowTopic.send_message)
    dp.register_message_handler(send_message, lambda message: message.text == "Отправить сообщение",
                                state=ShowTopic.topic_func)
    dp.register_message_handler(enter_message, state=ShowTopic.enter_message)
    # dp.register_message_handler(send_message, lambda message: message.text == "Отправить сообщение",
    #                             state=ShowTopic.topic_func)
    # dp.register_message_handler(send_message, lambda message: message.text == "Отправить сообщение",
    #                             state=ShowTopic.topic_func)
    # dp.register_message_handler()
