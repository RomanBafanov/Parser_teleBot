from aiogram.filters.command import Command
from utils.set_bot_commands import set_bot_commands
from loader import dp, bot
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import  F


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await set_bot_commands(bot)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Парсинг", callback_data="Парсинг")
    )
    builder.row(types.InlineKeyboardButton(
        text="История", callback_data="История")
    )
    await message.answer("Выберите действие", reply_markup=builder.as_markup())


@dp.callback_query(F.data == "/start")
async def cmd_start(callback: types.CallbackQuery):
    await set_bot_commands(bot)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Парсинг", callback_data="Парсинг")
    )
    builder.row(types.InlineKeyboardButton(
        text="История", callback_data="История")
    )
    await callback.message.answer("Выберите действие", reply_markup=builder.as_markup())