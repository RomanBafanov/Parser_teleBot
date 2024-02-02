from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.cities import search_cities
from loader import dp
from utils.statesform import StepsForm
from database.PARSER import get_vacancies_hh, filter_and_create_dict
from aiogram import F

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
        f' Введите название вакансии: (например, "PHP-разработчик")', reply_markup=builder.as_markup())
    await state.set_state(StepsForm.GET_VACANCY)


@dp.message(StepsForm.GET_VACANCY)
async def search_vacancy_name2(message: types.Message, state: FSMContext):
    global KEYWORD
    KEYWORD = message.text
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Назад", callback_data="Парсинг")
    )
    builder.row(types.InlineKeyboardButton(
        text="Продолжить", callback_data="Парс")
    )
    await message.answer(f"Введенный  - {KEYWORD}", reply_markup=builder.as_markup())
    await state.clear()


@dp.callback_query(F.data == "Парс")
async def get_data(callback: types.CallbackQuery):
    global KEYWORD
    global AREA
    try:
        vacancies_data = get_vacancies_hh(KEYWORD, AREA)  # Передаем переменные
        result = filter_and_create_dict(vacancies_data)
        print(result)
        for company in result:
            print(f"**Компания:** {company['Компания']}")
            print(f"Сайт: {company['Сайт']}")
            if company.get('Телефон'):
                print(f"Телефон: {company['Телефон']}")
            print()

        await callback.message.answer("Результаты выведены в терминал")
    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")

