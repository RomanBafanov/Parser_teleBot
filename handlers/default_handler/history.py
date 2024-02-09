from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import dp, bot
from utils.statesform import StepsForm
from aiogram import F
from aiogram.types import FSInputFile
from database.response import *
from database.cities import search_cities
from openpyxl import Workbook
import os.path
# import logging


# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s %(levelname)-8s %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )

CITY_CODE = None
TITLE_JOB = None


@dp.callback_query(F.data == "История")
async def search_response_history(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Список городов", callback_data="Города")
    )
    builder.row(types.InlineKeyboardButton(
        text="История запросов", callback_data="История запросов")
    )
    await callback.message.answer("Посмотрите нужный id города или проверте историю запросов",
                                  reply_markup=builder.as_markup())


@dp.callback_query(F.data == "Города")
async def search_id_city(callback: types.CallbackQuery):
    result = search_cities()
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Назад", callback_data="История")
    )
    message = ""
    for results in result:
        id_city = results[0]
        city = results[1]
        message += f"код : {id_city}  город: {city}\n\n"

    await callback.message.answer(message, reply_markup=builder.as_markup())


@dp.callback_query(F.data == "История запросов")
async def get_vacancies(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите код города:")
    await state.set_state(StepsForm.GET_CITY_ID)


@dp.message(StepsForm.GET_CITY_ID)
async def search_city_code(message: types.Message, state: FSMContext):
    global CITY_CODE
    CITY_CODE = message.text
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Назад", callback_data="История")
    )
    await message.answer(f"Введенный код города - {CITY_CODE}")
    await message.answer(
        f' Введите название вакансии: (например, Python-разработчик)', reply_markup=builder.as_markup())
    await state.set_state(StepsForm.GET_VACANCY_HISTORY)


@dp.message(StepsForm.GET_VACANCY_HISTORY)
async def search_vacancy_name2(message: types.Message, state: FSMContext):
    global TITLE_JOB
    TITLE_JOB = message.text
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Назад", callback_data="История")
    )
    builder.row(types.InlineKeyboardButton(
        text="Продолжить", callback_data="get_data_history")
    )
    await message.answer(f"Введенная вакансия  - {TITLE_JOB}", reply_markup=builder.as_markup())
    await state.clear()


@dp.callback_query(F.data == "get_data_history")
async def get_data_history(callback: types.CallbackQuery):
    await callback.message.answer("Обработка данных ...\n"
                                  "Пожалуйста подождите!\n")

    try:
        # print(f"Значение переменной CITY_CODE: {CITY_CODE}")
        # print(f"Значение переменной TITLE_JOB: {TITLE_JOB}")
        result = search_response_history1(CITY_CODE, TITLE_JOB)

        wb = Workbook()

        sheet = wb.active

        sheet.cell(row=1, column=1).value = "Компания"
        sheet.cell(row=1, column=2).value = "Сайт"
        sheet.cell(row=1, column=3).value = "Телефон"

        last_row = sheet.max_row + 1  # Определение номера строки для начала заполнения данных
        for row_index, row in enumerate(result, start=last_row):
            company, website, phone_number = row
            sheet.cell(row=row_index, column=1).value = company
            sheet.cell(row=row_index, column=2).value = website
            sheet.cell(row=row_index, column=3).value = phone_number

        for column in sheet.columns:
            max_length = 0
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except Exception as e:
                    await callback.message.answer(f"Ошибка: {e}")
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[column[0].column_letter].width = adjusted_width

        wb.save("history.xlsx")
        absolute_path = os.path.abspath("output.xlsx")
        document = FSInputFile(absolute_path)
        await bot.send_document(chat_id=callback.from_user.id, document=document)
    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")
