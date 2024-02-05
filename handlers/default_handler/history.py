from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.cities import search_cities
from loader import dp, bot
from utils.statesform import StepsForm
from database.PARSER import get_vacancies_hh, filter_and_create_dict
from aiogram.types import FSInputFile
from aiogram import F
import pandas as pd
import openpyxl
import os.path
import datetime
from database.requests import *


AREA = None
KEYWORD = None


@dp.callback_query(F.data == "История")
async def search_response_history(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите код города:")
    await state.set_state(StepsForm.GET_CITY_ID)


@dp.message(StepsForm.GET_CITY_ID)
async def search_city_code(message: types.Message, state: FSMContext):
    global AREA
    AREA = message.text
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Назад", callback_data="История")
    )
    await message.answer(f"Введенный код города - {AREA}")
    await message.answer(
        f' Введите название вакансии: (например, Python-разработчик)', reply_markup=builder.as_markup())
    await state.set_state(StepsForm.GET_VACANCY_HISTORY)


@dp.message(StepsForm.GET_VACANCY_HISTORY)
async def search_vacancy_name2(message: types.Message, state: FSMContext):
    global KEYWORD
    KEYWORD = message.text
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Назад", callback_data="История")
    )
    builder.row(types.InlineKeyboardButton(
        text="Продолжить", callback_data="get_data_history")
    )
    await message.answer(f"Введенная вакансия  - {KEYWORD}", reply_markup=builder.as_markup())
    await state.clear()


@dp.callback_query(F.data == "get_data_history")
async def search_response_history(callback: types.CallbackQuery, state: FSMContext):
    global AREA
    global KEYWORD
