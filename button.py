from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def confirm():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton('Подтвердить вход'))
    return m


def main_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton('Создать шаблон поста'))
    m.insert(KeyboardButton('Обновить приветственный пост'))
    m.add(KeyboardButton('Рассылка'))
    return m