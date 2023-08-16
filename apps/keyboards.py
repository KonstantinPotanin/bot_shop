from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(resize_keyboard=True)    # Чтобы клавиатура подстраивалась под размер устройства
main.add('Каталог').add('Корзина').add('Контакты')  # Клавиатура для пользователя

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку')  # После нажатия кнопки Админ-панель появится эта клавиатура


catalog_list = InlineKeyboardMarkup(row_width=2)    # Две кнопки в одной строчке
catalog_list.add(InlineKeyboardButton(text='Футболки', callback_data='t-shirt'),            # можно передать колбэк данные (то есть это функция которая передается на вход другой функции чтобы её запустили в ответ на какое-то событие
                 InlineKeyboardButton(text='Шорты', callback_data='shorts'),
                 InlineKeyboardButton(text='Кроссовки', url='https://youtube.com/@sudoteach'))    # можно передать ссылку

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')