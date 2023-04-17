from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import db


def confirm():
    if db.get_button():
        button_list = list()
        for button in db.get_button():
            button_list.append(button[1])

        m = ReplyKeyboardMarkup(resize_keyboard=True)
        m.add(KeyboardButton(button_list[0]))
        m.add(KeyboardButton(button_list[1]))
        m.add(KeyboardButton(button_list[2]))
        m.add(KeyboardButton(button_list[3]))
        return m
    else:
        m = ReplyKeyboardMarkup(resize_keyboard=True)
        m.add(KeyboardButton("Подтвердите вход"))
        m.add(KeyboardButton("Подтвердите вход"))
        m.add(KeyboardButton("Подтвердите вход"))
        m.add(KeyboardButton("Подтвердите вход"))
        return m


def main_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton('Создать шаблон поста'))
    m.insert(KeyboardButton('Обновить приветственный пост'))
    m.add(KeyboardButton('Рассылка'))
    m.insert(KeyboardButton('Изменить текст кнопок'))
    m.add(KeyboardButton('Добавить кнопку (только первое включение)'))
    return m