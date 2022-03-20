from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import types, Bot
from aiogram.dispatcher.filters import Text

from keyboards.keyboards import topics_keyboard, topic_info_keyboard, main_keyboard
from database.DataBaseRunner import DataBaseRunner
from .state_machine import ShowTopic, AppStates

db_runner = DataBaseRunner()
global_dispatcher: Dispatcher = None
global_bot: Bot = None


async def show_topics(message: types.Message, state: FSMContext) -> None:
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
            global_dispatcher.register_message_handler(topic_info, Text(equals=topic.name),
                                                       state=ShowTopic.showing_topic)

        await message.answer("Список ваших статей", reply_markup=topics_keyboard([topic.name for topic in topics]))


async def topic_info(message: types.Message, state: FSMContext):
    """Function for getting info about current topic"""
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
    """Function for sending message to the author"""
    if message.text == "Отправить сообщение":
        await ShowTopic.next()
        await message.answer("Введите текст сообщения для рассылки", reply_markup=types.ReplyKeyboardRemove())


async def enter_message(message: types.Message, state: FSMContext):
    """Function for entering topic name for sending message"""
    async with state.proxy() as data:
        # print(data)
        topic = db_runner.get_topic_by_name(data['topic'])

        db_runner.add_message(message.text, topic.name, message.from_user.username)

        targ_receivers = topic.addressees
        # print(topic.addressees)

        text = f"#{topic.name}\n\n{message.text}"  # \n\nАвтор: @{topic.author.tgm_link}
        for receiver in targ_receivers:
            t_chat_id = receiver.chat_id
            await global_bot.send_message(chat_id=t_chat_id, text=text)

    await message.answer("Сообщение отправлено")
    await state.finish()
    await AppStates.showing_topics.set()

    await state.set_state(AppStates.showing_topics.state)

    await show_topics(message, state)


async def show_all_messages(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        topic = db_runner.get_topic_by_name(data['topic'])
        author = topic.author
        receivers = topic.addressees
        cur_user = db_runner.get_user_by_username(message.from_user.username)

        answer = f"#{topic.name}\n\n{topic.text}\n\n"

        if cur_user == author:
            # Выводим для автора
            for msg in topic.messages:
                if msg.sender == author:
                    answer += f"-> {msg.msg_text}\n"
                else:
                    answer += f"@{msg.sender.tgm_link}: {msg.msg_text}\n"

        elif cur_user in receivers:
            # Выводим сообщения авторов
            pass
        else:
            # Выводим только главное сообщение
            pass

        await ShowTopic.showing_topic.set()
        await message.answer(answer)

        message.text = topic.name
        await state.set_state(ShowTopic.showing_topic.state)

        await topic_info(message, state)


async def return_to_topics(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     if data.get("topic") is None:
    #         pass
    #     else:
    await state.finish()
    await AppStates.showing_topics.set()

    await state.set_state(AppStates.showing_topics.state)
    await show_topics(message, state)


async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Главное меню", reply_markup=main_keyboard())


def register_show_topics_handlers(dp: Dispatcher, bot: Bot) -> None:
    global global_dispatcher
    global_dispatcher = dp
    global global_bot
    global_bot = bot
    dp.register_message_handler(show_topics, state=AppStates.showing_topics)
    # dp.register_message_handler(lambda message: ShowTopic.send_message.set(),
    #                             lambda message: message.text == "Отправить сообщение")
    # dp.register_message_handler(send_message, state=ShowTopic.send_message)
    dp.register_message_handler(send_message, lambda message: message.text == "Отправить сообщение",
                                state=ShowTopic.topic_func)
    dp.register_message_handler(enter_message, state=ShowTopic.enter_message),
    dp.register_message_handler(return_to_topics, lambda message: message.text == "Вернуться к списку тем",
                                state=ShowTopic.topic_func)
    dp.register_message_handler(return_to_main_menu, lambda message: message.text == "Выйти", state="*")
    dp.register_message_handler(show_all_messages, lambda message: message.text == "Просмотреть все сообщения темы",
                                state=ShowTopic.topic_func)
    # dp.register_message_handler(send_message, lambda message: message.text == "Отправить сообщение",
    #                             state=ShowTopic.topic_func)
    # dp.register_message_handler(send_message, lambda message: message.text == "Отправить сообщение",
    #                             state=ShowTopic.topic_func)
    # dp.register_message_handler()
