from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.keyboards import main_keyboard, topics_keyboard
from functions import functions


class CreateTopicForm(StatesGroup):
    """
    Form for creating new topic
    """
    topic_name = State()
    message = State()
    addressees = State()
    # link = State()


class TopicForChangeAddressees(StatesGroup):
    topic_name = State()


class AddresseesForChange(StatesGroup):
    usernames = State()


async def start_command(message: types.Message) -> None:
    """
    Welcome
    :param message: start message
    """
    await message.answer("Добро пожаловать в бота-менеджера", reply_markup=main_keyboard())


async def view_topics(message: types.Message) -> None:
    """
    Function to view the list of topics
    :param message: message from user
    """
    topics = functions.get_topics(message.from_user.username)
    if topics is None:
        await message.answer("Вы не создали ещё ни одной темы")
    else:
        await message.answer("Список ваших статей", reply_markup=topics_keyboard(topics))


async def change_addressees(message: types.Message) -> None:
    """
    Function for changing addressees
    :param message: message from user
    """
    await TopicForChangeAddressees.topic_name.set()
    await message.answer("Для выхода из режима изменения адресатов введите команду /cancel")
    await message.answer("Введите название топика", reply_markup=types.ReplyKeyboardRemove())


async def enter_topic_for_change(message: types.Message, state: FSMContext) -> None:
    """
    Enter topic name for changing addressees
    :param message: message from user
    :param state: form state
    """
    topic = message.text
    if topic in functions.get_topics(message.from_user.username):
        async with state.proxy() as data:
            data['topic_name'] = message.text

        addressees = functions.get_addressees(data['topic_name'])

        await state.finish()
    else:
        await message.answer("У Вас нет такой темы")
        return


async def create_topic(message: types.Message) -> None:
    """
    Start creating a topic
    :param message: message from user
    """
    await CreateTopicForm.topic_name.set()
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
    await CreateTopicForm.next()
    await message.answer("Введите содержание письма")


async def enter_message(message: types.Message, state: FSMContext) -> None:
    """
    Enter message for distribution
    :param message: message containing the mailing text
    :param state: form state
    """
    async with state.proxy() as data:
        data['message'] = message.text
    await CreateTopicForm.next()
    await message.answer("Введите адресатов через \";\"")


async def enter_addressees(message: types.Message, state: FSMContext) -> None:
    """
    Enter message addressees
    :param message: message containing message addressees
    :param state: form state
    """
    async with state.proxy() as data:
        data['addressees'] = message.text.split(";")
        print(data)
    # add to DB and send messages
    await message.answer("Тема добавлена", reply_markup=main_keyboard())
    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    The function that handles the cancellation of data entry. Resets the state machine
    :param message: message from user
    :param state: current FSM state
    :return: no factory reset if state is empty
    """
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нечего отменять!")
        return
    await state.finish()
    await message.answer("Действия отменены", reply_markup=main_keyboard())


def register_admin_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(view_topics, lambda message: message.text == "Просмотреть все свои темы")
    dp.register_message_handler(create_topic, lambda message: message.text == "Добавить топик")
    dp.register_message_handler(enter_name, state=CreateTopicForm.topic_name)
    dp.register_message_handler(enter_message, state=CreateTopicForm.message)
    dp.register_message_handler(enter_addressees, state=CreateTopicForm.addressees)

    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(start_command, commands=['start'])
