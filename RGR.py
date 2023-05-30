import requests
import json
import os
import threading
import psycopg2 as pg
from datetime import date, timedelta

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

ALPHAVANTAGE_API_KEY = '9OZBY4NHW13I3EK4'
# Токен бота
API_TOKEN = '5979878197:AAF1PTvdw5BvjWTWwvaUld1Sv-jDh-7rjrM'
# Таймер для перерасчета показателей акций (24 часа)
WAIT_TIME_SECONDS = 60 * 24 *24
# Конфиг для локальной БД
conn = pg.connect(user='postgres', password='postgres', host='localhost', port='5432', database='TimShiv')
cursor = conn.cursor()


class Form(StatesGroup):
    save = State()
    show = State()


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# Раз в WAIT_TIME_SECONDS секунд пересчитываем показатели для всех бумаг
def periodically_recalculate_stocks():
    ticker = threading.Event()
    while not ticker.wait(WAIT_TIME_SECONDS):
        print("старт")
        recalculate_stocks()

# Функция возвращает строку с информацией о добавлении новой ценной бумаги к отслеживаемым
async def add_stock_bd(user_id, stock_name):
    data = get_values_and_averages(stock_name)
    cursor.execute(
        f"""SELECT * FROM stock
        WHERE user_id = {user_id}
        AND stock_name = '{stock_name}'"""
    )
    users = cursor.fetchall()
    if len(users) == 0:
        cursor.execute(
            f"""INSERT INTO stock (user_id, stock_name, averages_open,averages_close,max_price,min_price)
             VALUES ({user_id}, '{stock_name}', '{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}')"""
        )
        conn.commit()
        return f'Ценная бумага {stock_name} добавлена к отслеживаемым'
    else:
        cursor.execute(
            f"""UPDATE stock
            SET averages_open = '{data[0]}',
                averages_close = '{data[1]}',
                max_price = '{data[2]}',
                min_price = '{data[3]}'
            WHERE user_id = {user_id}
            AND stock_name = '{stock_name}'"""
        )
        conn.commit()
        return f'Ценная бумага {stock_name} обновлена'

# Определение функции, которая будет получать данные о ценных бумагах по их имени
def get_stocks_by_name(name):
# Исполнение SQL-запроса к базе данных, на основании имени ценной бумаги,
# получение ее основных параметров: названия, средних значений открытия и закрытия цены, максимальной и минимальной цены
    cursor.execute(
        f"""SELECT stock_name, averages_open, averages_close, max_price, min_price FROM stock
        WHERE stock_name = '{name}'"""
    )
# Получение результата SQL-запроса и сохранение в переменную stocks
    stocks = cursor.fetchall()
# Определение строки msg, которая будет сформирована на основе полученных данных
    msg = ''
# Итерация по набору данных о ценных бумагах, полученных из результата SQL-запроса
    for stock_name, averages_open, averages_close, max_price, min_price in stocks:
    # Если один из основных параметров ценной бумаги равен "null", то добавление сообщения об этом в строку msg
        if (averages_open or averages_close or max_price or min_price) == 'null':
            msg += f'Для ценной бумаги {stock_name} не найдено значений\n\n'
        else:
# Иначе, добавление информации о ценной бумаге в строку msg
            msg += f'Акция {stock_name} имеет\n' \
                   f'Cреднее значение открытия {averages_open}\n\n' \
                   f'Cреднее значение закрытия {averages_close}\n\n' \
                   f'Наибольшая цена бумаги {max_price}\n\n' \
                   f'Наименьшая цена бумаги {min_price}\n\n'
# Возвращение строки msg из функции get_stocks_by_name
    return msg

# Функция для пересчета запасов
def recalculate_stocks():
# Выбираем все строки из таблицы stock
    cursor.execute(
        f"""SELECT * FROM stock """
    )
# Получаем все строки из таблицы stock
    stocks = cursor.fetchall()
# Идем по каждой строке
    for stock in stocks:
# Получаем данные о запасах
        data = get_values_and_averages(stock[2])
# Обновляем данные в таблице stock
# Обновляем строки для пользователя с указанным id и названием запаса
        cursor.execute(
            f"""UPDATE stock
            SET averages_open = {data[0]},
                averages_close = {data[1]},
                max_price = {data[2]},
                min_price = {data[3]}
            WHERE user_id = {stock[0]} AND stock_name = '{stock[2]}'"""
        )


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    kb = ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True, row_width=1)
    kb.add(KeyboardButton('/Add'))
    kb.add(KeyboardButton('/Show'))

    await message.answer(text='Добро пожаловать в чат бот!', reply_markup=kb)


@dp.message_handler(commands=['Add'])
async def add_stock(message: Message):
    await message.answer('Введите имя ценной бумаги')
    await Form.save.set()


@dp.message_handler(state=Form.save)
async def save_stock(message: Message, state: FSMContext):
    ide = message.from_id
    print(ide)
    test = message.text
    print(test)
    msg = await add_stock_bd(ide, test)
    await message.answer(msg)
    await state.finish()


@dp.message_handler(commands=['Show'])
async def stock_get(message: Message):
    await message.answer('Введите название ценной бумаги')
    await Form.show.set()


@dp.message_handler(state=Form.show)
async def save_stock(message: Message, state: FSMContext):
    msg = get_stocks_by_name(message.text)
    await message.answer(msg)
    await state.finish()


def fetch_data(company_symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={company_symbol}&apikey={ALPHAVANTAGE_API_KEY}"
    response = requests.get(url)
    return json.loads(response.text)


def get_values_and_averages(company_symbol):
    data = fetch_data(company_symbol)

    # Если компания не найдена, возвращаем налы
    if data.get('Error Message'):
        return 'null', 'null, null, null'

    # Длина периода для рассчета среднего
    n = 30
    # Счетчик отступа дней от сегодня
    day_offset = 0
    # Счетчик дней, для которых удалось получить данные
    days_counted = 0

    # Массив с датами
    dates = []
    # Здесь храним средние значения по периодам длиной n
    val1 = float()
    val2 = float()
    min_val = float(1000)
    max_val = float()
    avg_open = 0
    avg_close = 0

    while day_offset < n:
        day = (date.today() - timedelta(days=day_offset)).isoformat()
        day_info = data['Time Series (Daily)'].get(day)
        day_offset += 1

        # Пропускаем день, если по нему нет данных
        if day_info is None:
            continue

        # Достаем значение ценности бумаги
        val1 += float(day_info['1. open'])
        val_max = float(day_info['2. high'])
        val_min = float(day_info['3. low'])
        val2 += float(day_info['4. close'])

        if max_val < val_max:
            max_val = val_max

        if min_val > val_min:
            min_val = val_min

        avg_open = val1 / 30
        avg_close = val2 / 30

    return avg_open, avg_close, max_val, min_val


if __name__ == '__main__':
    thread = threading.Thread(target=periodically_recalculate_stocks)
    thread.start()
    executor.start_polling(dp, skip_updates=True)
