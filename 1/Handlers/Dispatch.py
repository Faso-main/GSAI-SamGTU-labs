from aiogram import types, Router
from aiogram.filters.command import Command
from Handlers.Keyboards import create_keyboard


router3=Router()

@router3.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard=create_keyboard()
    await message.answer(
        "Привет! Я бот для помощи абитуриентам и студентам САМГТУ, ты можешь обратиться ко мне с любым вопросом,"
        " и я очень постараюсь ответить тебе на него \U0001F49C \U0001F4AB",
        reply_markup=keyboard
        )
def register_handlers(router: Router):
    router.include_router(router3)
