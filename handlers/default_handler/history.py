from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import dp
from utils.statesform import StepsForm
from aiogram import F
from database.response import search_response_history
from database.cities import search_cities

AREA = None
KEYWORD = None


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
async def search_history(callback: types.CallbackQuery):
    global AREA
    global KEYWORD
    await callback.message.answer("Обработка данных с hh.ru...\n"
                                  "Пожалуйста подождите!\n")

    try:
        response_history = search_response_history(AREA, KEYWORD)
        print(response_history)
        # for company, company_info in companies.items():
        #     insert_response_data(id_request, company, company_info['Сайт'], company_info['Телефон'])
        #
        # # Создаем DataFrame из списка словарей
        # df = pd.DataFrame(list(companies.values()), index=companies.keys(), columns=['Сайт', 'Телефон'])
        #
        # # Сохраняем DataFrame в Excel
        # df.to_excel('output.xlsx', index_label='Компания')
        #
        # # Открываем файл Excel
        # wb = openpyxl.load_workbook('output.xlsx')
        #
        # # Выбираем активный лист (первый лист в книге)
        # sheet = wb.active
        #
        # # Устанавливаем ширину столбцов
        # sheet.column_dimensions['A'].width = 30
        # sheet.column_dimensions['B'].width = 30
        # sheet.column_dimensions['C'].width = 30
        #
        # # Устанавливаем высоту строк
        # sheet.row_dimensions[1].height = 15
        # sheet.row_dimensions[2].height = 15
        #
        # # Сохраняем изменения в файл
        # wb.save('output.xlsx')
        # absolute_path = os.path.abspath("output.xlsx")
        # document = FSInputFile(absolute_path)
        await callback.message.answer("yytytyy")
    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")
