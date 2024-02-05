from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_VACANCY = State()
    GET_ID_CITY = State()
    GET_CITY_ID = State()
    GET_VACANCY_HISTORY = State()