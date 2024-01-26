from aiogram import F
from loader import dp
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(F.data == "Парсинг")
async def publication_new_products(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Список городов", callback_data="Список городов")
    )
    builder.row(types.InlineKeyboardButton(
        text="Получить данные", callback_data="Получить данные")
    )
    await callback.message.answer("Посмотрите нужный id города или начните Парсинг",
                                  reply_markup=builder.as_markup())
