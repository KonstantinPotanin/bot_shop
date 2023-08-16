import sqlite3 as sq

db = sq.connect('tg.db')    # создание файла в корневом каталоге, если бы файл был в папке apps, то в скобках было
                            # Написано - apps/tg.db. Если файла нет он создается, если есть, то к нему подключается.
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("      # Создать таблицу если её не существует, которая называется - accounts
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "    # Перечислены ряды в этой таблице 1 - id; 2 - то что добавлено в корзину
                "tg_id INTEGER, "
                "cart_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS items("         # Также создана таблица, с соответствующими столбцами
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT,"
                "desc TEXT, "
                "price TEXT, "
                "photo TEXT, "
                "brand TEXT)")
    db.commit()


async def cmd_start_db(user_id):                           # Кто вошел в наш бот и написал коммаду /start далее можно обращаться по этому ИД и делать например рассылку
    user = cur.execute('SELECT * FROM accounts WHERE tg_id == {key}'.format(key=user_id)).fetchone()    # передаем user_id если этот ИД есть то ок
    if not user:                                                                                        # если нет, то добавляем
        cur.execute('INSERT INTO accounts (tg_id) VALUES ({key})'.format(key=user_id))
        db.commit()                                                                                     # commit сохраняет изменения
                                                                                                        # добовляем к комманде /start


async def add_item(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)",
                    (data['name'], data['desc'], data['price'], data['photo'], data['type']))
        db.commit()