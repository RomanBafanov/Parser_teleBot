from aiogram import F
from loader import dp
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(F.data == "История")
async def publication_new_products(callback: types.CallbackQuery):
    await callback.message.answer("История запросов")
