from aiogram import Bot
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

import button
import config
import db

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Bot is running')
    db.start_db()


class MassSend(StatesGroup):
    sendd1 = State()
    sendd2 = State()


class saveMessage(StatesGroup):
    sv_mess1 = State()
    sv_mess2 = State()
    sv_mess3 = State()


class welcomePost(StatesGroup):
    wl_post1 = State()


class buttonText(StatesGroup):
    b_text = State()
    b_text1 = State()


class buttonAdd(StatesGroup):
    b_add = State()


@dp.message_handler(commands='start', user_id=config.ADMIN_ID)
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, text="Добро пожаловать!", reply_markup=button.main_menu())


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, text="Добро пожаловать!")


@dp.chat_join_request_handler()
async def chat_join_request_handler(chat_join_request: types.ChatJoinRequest):
    chat_member = await bot.get_chat_member(chat_join_request.chat.id, chat_join_request.from_user.id)
    user_id = chat_join_request.user_chat_id
    chat_id = chat_join_request.chat.id
    db.add_channel(chat_join_request.chat.id, chat_join_request.chat.title)

    print(f'user_id - {user_id}')
    print(f'chat_id - {chat_id}')
    db.add_await_user(chat_id, user_id)
    data = db.get_welcome_post()
    await bot.copy_message(chat_id=chat_join_request.from_user.id, from_chat_id=data[0][0], message_id=data[0][1],
                           reply_markup=button.confirm())


@dp.message_handler(lambda message: message.text in db.handler_button_words())
async def approve_join_request(message: types.Message):
    print(f'DB input - {db.inpt(message.chat.id)}')
    data = db.inpt(message.chat.id)
    chat_id = data[1]
    user_id = data[2]
    await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
    db.add_user(user_id, chat_id)
    db.clear(message.chat.id)
    await bot.send_message(chat_id=message.chat.id, text="Ваш запрос на вход в чат был принят!")


@dp.message_handler(text='Обновить приветственный пост', user_id=config.ADMIN_ID)
async def welcome_post(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=f'Пришлите приветственный пост: ')
    await welcomePost.wl_post1.set()


@dp.message_handler(state=welcomePost.wl_post1)
async def save_welcome_post(message: types.Message, state: FSMContext):
    db.edit_welcome_post(message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, text=f'Приветственный пост добавлен', reply_markup=button.main_menu())
    await state.finish()


@dp.message_handler(text='Создать шаблон поста', user_id=config.ADMIN_ID)
async def create_post(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=f'Пришлите название шаблона: ')
    await saveMessage.sv_mess1.set()


@dp.message_handler(state=saveMessage.sv_mess1)
async def save_sample_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await saveMessage.next()
    await bot.send_message(message.chat.id, text='Пришлите пост:')


@dp.message_handler(state=saveMessage.sv_mess2)
async def save_sample(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        title = data.get('title')
    db.add_message(title, message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, text=f'Вы успешно добавили шаблон поста под названием "{title}"',
                           reply_markup=button.main_menu())
    await state.finish()


@dp.message_handler(text='Добавить кнопку (только первое включение)', state=None, user_id=config.ADMIN_ID)
async def button_add(message: types.Message):
    await bot.send_message(message.from_user.id, text=f"* Добавить кнопок можно всего 4 шт *\n"
                                                      f"* Эта функция делается только при первом включении бота *\n"
                                                      f"* В дальнейшем просто редактируйте их текст *")
    await buttonAdd.b_add.set()
    await bot.send_message(message.from_user.id, text=f"Введите текст кнопки:")


@dp.message_handler(state=buttonAdd.b_add)
async def button_add(message: types.Message, state: FSMContext):
    text = message.text
    if db.add_button(text):
        await state.finish()
        await bot.send_message(message.from_user.id, text=f"Добавлена кнопка '{text}'",
                               reply_markup=button.main_menu())
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, text=f"Достигнут лимит кнопок (4 штуки)",
                               reply_markup=button.main_menu())


@dp.message_handler(text='Изменить текст кнопок', state=None, user_id=config.ADMIN_ID)
async def button_txt_edit(message: types.Message, state: FSMContext):
    if db.get_button():
        await bot.send_message(message.from_user.id, text=f"Введите ID кнопки:")
        for i in db.get_button():
            await bot.send_message(message.chat.id, text=f'ID: {i[0]}\n'
                                                         f'Текст кнопки: {i[1]}')
        await buttonText.b_text.set()
    else:
        await bot.send_message(message.from_user.id, text=f"Кнопок не создано")


@dp.message_handler(state=buttonText.b_text)
async def button_id_save(message: types.Message, state: FSMContext):
    number = message.text
    if number.isdigit():
        async with state.proxy() as data:
            data['button_id'] = number
        await bot.send_message(message.chat.id, text='Теперь введите текст: ')
        await buttonText.next()
    else:
        await state.finish()
        await bot.send_message(message.chat.id, text='Вы ввели не цифру!', reply_markup=button.main_menu())


@dp.message_handler(state=buttonText.b_text1)
async def button_txt_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        button_id = data.get('button_id')
    button_text = message.text
    db.update_button_text(button_id, button_text)
    await state.finish()
    await bot.send_message(message.chat.id, text='Текст кнопки успешно изменен 👍', reply_markup=button.main_menu())


@dp.message_handler(text='Рассылка', state=None, user_id=config.ADMIN_ID)
async def sample(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text=f"Введите ID шаблона для отправки:")
    if db.get_message():
        for i in db.get_message():
            await bot.send_message(message.chat.id, text=f'ID: {i[0]}\n'
                                                         f'Имя шаблона: {i[1]}')
        await MassSend.sendd1.set()
    else:
        await state.finish()
        await bot.send_message(message.chat.id, text='Вы не добавили ни одного шаблона')


@dp.message_handler(state=MassSend.sendd1)
async def select_channel(message: types.Message, state: FSMContext):
    number = message.text
    if number.isdigit():
        await bot.send_message(message.chat.id, text='Шаблон выбран 👍')
        async with state.proxy() as data:
            data['sample_id'] = message.text
        await bot.send_message(message.chat.id, text='Теперь введите ID канала:')
        if db.get_message():
            for i in db.get_channel():
                await bot.send_message(message.chat.id, text=f'ID: {i[0]}\n'
                                                             f'Имя канала: {i[2]}')
            await MassSend.next()
        else:
            await state.finish()
            await bot.send_message(message.chat.id, text='Вы не добавили ни одного шаблона',
                                   reply_markup=button.main_menu())
    else:
        await state.finish()
        await bot.send_message(message.chat.id, text='Вы ввели не цифру!', reply_markup=button.main_menu())


@dp.message_handler(state=MassSend.sendd2)
async def send(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        sample_id = data.get('sample_id')
    chan_id = message.text
    await state.finish()
    if chan_id.isdigit():
        data = db.template_selection(int(sample_id))
        print(data)
        if data:
            good, bad = 0, 0
            await state.finish()
            errors_list = []
            for i in db.get_users_in_channel_id(chan_id):
                try:
                    await bot.copy_message(chat_id=i[0], from_chat_id=message.chat.id, message_id=data[0][3],
                                           reply_markup=button.main_menu())
                    good += 1
                except Exception as e:
                    bad += 1
                    errors_list.append(e)
            await bot.send_message(message.from_user.id, 'Рассылка завершена успешно\n'
                                                         f'Доставлено: {good}\n'
                                                         f'Не доставлено: {bad}\n'
                                                         f'Ошибки {set(errors_list)}',
                                   reply_markup=button.main_menu())
        else:
            await bot.send_message(message.chat.id, text='Шаблон указан не верно, рассылка невозможна',
                                   reply_markup=button.main_menu())  # menu button
    else:
        await bot.send_message(message.chat.id, text='Вы ввели не цифру!', reply_markup=button.main_menu())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
