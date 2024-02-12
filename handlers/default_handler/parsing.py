from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.cities import search_cities
from loader import dp, bot
from utils.statesform import StepsForm
from parser import get_companies
from aiogram.types import FSInputFile
from aiogram import F
import pandas as pd
import openpyxl
import os.path
import datetime
from database.requests import *
from database.response import *


AREA = None
KEYWORD = None


@dp.callback_query(F.data == "Парсинг")
async def parsing(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Список городов", callback_data="Список городов")
    )
    builder.row(types.InlineKeyboardButton(
        text="Получить данные", callback_data="Получить данные")
    )
    await callback.message.answer("Посмотрите нужный id города или начните Парсинг",
                                  reply_markup=builder.as_markup())


@dp.callback_query(F.data == "Список городов")
async def search_id_city(callback: types.CallbackQuery):
    result = search_cities()
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Назад", callback_data="Парсинг")
    )
    message = ""
    for results in result:
        id_city = results[0]
        city = results[1]
        message += f"код : {id_city}  город: {city}\n\n"

    await callback.message.answer(message, reply_markup=builder.as_markup())


@dp.callback_query(F.data == "Получить данные")
async def get_vacancies(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите код города:")
    await state.set_state(StepsForm.GET_ID_CITY)


@dp.message(StepsForm.GET_ID_CITY)
async def search_city_code(message: types.Message, state: FSMContext):
    global AREA
    AREA = message.text
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Назад", callback_data="Парсинг")
    )
    await message.answer(f"Введенный код города - {AREA}")
    await message.answer(
        f' Введите название вакансии: (например, Python-разработчик)', reply_markup=builder.as_markup())
    await state.set_state(StepsForm.GET_VACANCY)


@dp.message(StepsForm.GET_VACANCY)
async def search_vacancy_name2(message: types.Message, state: FSMContext):
    global KEYWORD
    KEYWORD = message.text.capitalize()
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Назад", callback_data="Парсинг")
    )
    builder.row(types.InlineKeyboardButton(
        text="Продолжить", callback_data="get_data")
    )
    await message.answer(f"Введенная вакансия  - {KEYWORD}", reply_markup=builder.as_markup())
    await state.clear()


@dp.callback_query(F.data == "get_data")
async def get_data(callback: types.CallbackQuery):
    global KEYWORD
    global AREA
    date = datetime.datetime.now()
    await callback.message.answer("Обработка данных ...\n"
                                  "Пожалуйста подождите\n")
    try:

        companies = get_companies(KEYWORD, AREA)
        id_request = insert_requests_data(AREA, KEYWORD, date)
        for company, company_info in companies.items():
            insert_response_data(id_request, company, company_info['Сайт'], company_info['Телефон'])

        # Создаем DataFrame из списка словарей
        df = pd.DataFrame(list(companies.values()), index=companies.keys(), columns=['Сайт', 'Телефон'])

        # Сохраняем DataFrame в Excel
        df.to_excel('output.xlsx', index_label='Компания')

        # Открываем файл Excel
        wb = openpyxl.load_workbook('output.xlsx')

        # Выбираем активный лист (первый лист в книге)
        sheet = wb.active

        # Устанавливаем ширину столбцов
        sheet.column_dimensions['A'].width = 30
        sheet.column_dimensions['B'].width = 30
        sheet.column_dimensions['C'].width = 30

        # Устанавливаем высоту строк
        sheet.row_dimensions[1].height = 15
        sheet.row_dimensions[2].height = 15

        # Сохраняем изменения в файл
        wb.save('output.xlsx')
        absolute_path = os.path.abspath("output.xlsx")
        document = FSInputFile(absolute_path)
        await bot.send_document(chat_id=callback.from_user.id, document=document)
    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")