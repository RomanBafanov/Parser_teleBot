from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_VACANCY = State()
    GET_ID_CITY = State()