from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup     # создает наше состояние
from aiogram.dispatcher import FSMContext
from apps import keyboards as kb
from apps import database as db
from dotenv import load_dotenv
import os


async def on_start(_):
    await db.db_start()         # чтобы функция запускалась во время запуска бота
    print('Заработало!!!')

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


class NewOrder(StatesGroup):
    type = State()              # состояния
    name = State()
    desc = State()
    price = State()
    photo = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)     # проверяет есть этот юзер в базе данных
    await message.answer_sticker('CAACAgIAAxkBAAMlZNuajKiAUPFwS_NdV5wQg7scwB8AAgEAA8A2TxMYLnMwqz8tUTAE')    # ID стикера который нас встречает после комманды /start
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в магазин кроссовок!', reply_markup=kb.main)   #Клавиатура появится когда пользователь напишет комманду /start
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизовались как администратор!', reply_markup=kb.main_admin)


@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer(f'Каталог пуст!', reply_markup=kb.catalog_list)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пустая')


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Покупать товары у него: @kostia_po')


@dp.message_handler(text='Админ-панель')
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer(f'Выберите тип товара', reply_markup=kb.catalog_list)
    else:
        await message.reply('Я тебя не понимаю.')


# @dp.message_handler(content_types=['sticker'])
# async def check_sticker(message: types.Message):
#     await message.answer(message.sticker.file_id)
#     await bot.send_message(message.from_user.id, message.chat.id)
#
#
# @dp.message_handler(content_types=['document', 'photo'])
# async def forward_message(message: types.Message):
#     await bot.forward_message(os.getenv('GROUP_ID'), message.from_user.id, message.message_id)

@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):  # для того чтобы запоминать что мы выбрали
    async with state.proxy() as data:
        data['type'] = call.data        # запоминает в переменную data под ключом type то что отправили в call.data
    await call.message.answer(f'Напишите название товара', reply_markup=kb.cancel)
    await NewOrder.next()           # идёт дальше к следующему состоянию


@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Напишите описание товара')
    await NewOrder.next()            # идёт дальше к следующему состоянию


@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Напишите цену товара')
    await NewOrder.next()            # идёт дальше к следующему состоянию


@dp.message_handler(state=NewOrder.price)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте фотографию товара')
    await NewOrder.next()            # идёт дальше к следующему состоянию


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Это не фотография!')


@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer('Товар успешно создан!', reply_markup=kb.admin_panel)
    await state.finish()


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю')


@dp.callback_query_handler()        # декоратор или обработчик
async def callback_query_keyboards(callback_query: types.CallbackQuery):    # в параметры обработчика нельзя передавать Message
    if callback_query.data == 't-shirt':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали футболки') # Использует bot и указываем кому будум отправлять сообщение
    elif callback_query.data == 'shorts':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали шорты')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
