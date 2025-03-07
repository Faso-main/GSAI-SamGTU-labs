from aiogram import types,Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove


router2=Router()


reply_to_help='Чтобы задать мне вопрос, нажми на кнопку "Задать вопрос" в меню\nБуду рад помочь!😄'

@router2.message(Command("help"))
async def answer_on_help(message: types.Message,state:FSMContext):
    await state.clear()
    await message.answer(text=reply_to_help, reply_markup=ReplyKeyboardRemove())

@router2.message(F.text)
async def answer_on_help(message: types.Message,state:FSMContext):
    await state.clear()
    await message.answer(text=reply_to_help, reply_markup=ReplyKeyboardRemove())


def register_handlers(router: Router):
    router.include_router(router2)
