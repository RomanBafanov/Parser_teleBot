from aiogram.filters.command import Command
from utils.set_bot_commands import set_bot_commands
from loader import dp, bot
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
