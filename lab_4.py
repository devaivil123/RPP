import os
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(token='5979878197:AAF1PTvdw5BvjWTWwvaUld1Sv-jDh-7rjrM')
dp = Dispatcher(bot)

# Опредение названия валют и их курсы
RUB = 'RUB'
USD = 'USD'

RUB_TO_USD = 0.013
USD_TO_RUB = 75.69

# Определите глобальные переменные для хранения пользовательских входных данных
curr_name = None
curr_amount = None


# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Я бот, который умеет конвертировать валюты. Для начала, напиши обозначение валюты, например, 'USD' или 'RUB'. (Пока только имеено такие названия :/)")


# Обработчик для команды /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Я помогу тебе конвертировать из RUB в USD и наоборот. Просто напиши обозначение валюты, например, 'USD'.")


# Обработчик вводов пользователя
@dp.message_handler()
async def handle_user_input(message: types.Message):
    global curr_name, curr_amount

    if curr_name is None:
        # Пользователь вводит название валюты
        curr_name = message.text.upper()  # Преобразовать в верхний регистр для недопущения ошибок ввода

        # Проверка на действительность ввода валюты
        if curr_name not in [RUB, USD]:
            await message.reply(f"Неправильное обозначение валюты: {curr_name}")
            curr_name = None  # Сброс названия валюты для следующего ввода
        else:
            await message.reply(f"Хорошо, а теперь напиши кол-во {curr_name} для конвертации")
    else:
        # Пользователь вводит сумму в валюте
        try:
            curr_amount = float(message.text)
            if curr_name == RUB:
                # Convert RUB to USD
                usd_amount = curr_amount * RUB_TO_USD
                await message.reply(f"{curr_amount:.2f} {RUB} = {usd_amount:.2f} {USD}")
                await message.reply(f"Для повторной конвертации напишите новое название валюты или команду /start")
            else:
                # Конвертация доллара в рубль
                rub_amount = curr_amount * USD_TO_RUB
                await message.reply(f"{curr_amount:.2f} {USD} = {rub_amount:.2f} {RUB}")
                await message.reply(f"Для повторной конвертации напишите новое название валюты или команду /start")
        except ValueError:
            await message.reply("Неправильный формат числа")
        except Exception as e:
            await message.reply(f"Произошла ошибка: {e}")

        # Сброс переменных для следующего ввода
        curr_name = None
        curr_amount = None

# Запуск бота для дальнейшей работы
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)