from aiogram import types, Router
from aiogram.filters.command import Command
from Handlers.Keyboards import create_keyboard


router_dispatch=Router()

@router_dispatch.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard=create_keyboard()
    await message.answer(
        "Привет! Я бот TTT, делаю, что хочу",
        reply_markup=keyboard
        )

