from aiogram import types, Router
from aiogram.filters.command import Command
from Handlers.Keyboards import create_keyboard


router3=Router()

@router3.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard=create_keyboard()
    await message.answer(
        "Привет! Я бот Говорун, говорю что хочу и когда хочу",
        reply_markup=keyboard
        )
def register_handlers(router: Router):
    router.include_router(router3)
