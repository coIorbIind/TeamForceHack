from aiogram.dispatcher.filters.state import StatesGroup, State


class AppStates(StatesGroup):
    """Main state Machine"""
    #start_state = State() # Нужно ли?
    adding_topic = State()
    showing_topics = State()
    send_message_to_author = State()


class CreateTopic(StatesGroup):
    """Form for creating new topic"""
    topic_name = State()
    message = State()
    addressees = State()


class ShowTopic(StatesGroup):
    """Topic info states"""
    showing_topic = State()
    topic_func = State()
    enter_message = State()
    # change_addressees = State()
    # send_message = State()
    # show_messages = State()


class ChangeAddressees(StatesGroup):
    """States for changing """
    addressees_for_add = State()
    addressees_for_delete = State()


class SendMessageToTopic(StatesGroup):
    enter_topic = State()
    enter_message = State()
