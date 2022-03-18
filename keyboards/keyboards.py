from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    Main client keyboard
    :return: keyboard
    """
    add_button = KeyboardButton("Добавить топик")
    view_button = KeyboardButton("Просмотреть все свои темы")
    change_addressees_button = KeyboardButton("Изменить адресатов")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(add_button)
    keyboard.add(view_button)
    keyboard.add(change_addressees_button)
    return keyboard


def topics_keyboard(topics: list) -> ReplyKeyboardMarkup:
    """
    Creating keyboard to switch between topics
    :param topics: topics for creating keyboard
    :return: topic's keyboard
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for item in topics:
        keyboard.add(KeyboardButton(item))

    return keyboard


def change_addressees_keyboard(flag: bool) -> ReplyKeyboardMarkup:
    """
    Keyboard for changing addressees of topic
    :param flag: if flag is True we can delete users, else addressees are top
    :return: keyboard
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    if flag:
        delete_button = KeyboardButton("Удалить получателя")
        keyboard.add(delete_button)

    add_button = KeyboardButton("Добавить получателя")

    keyboard.add(add_button)

    return keyboard
