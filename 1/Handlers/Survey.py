from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from Handlers.Keyboards import create_keyboard, make_row_keyboard
from LLM.Train_Save_Bert import response
from datetime import datetime, timedelta
from Handlers.Bot_State import Bot_State
from aiogram.types import ReplyKeyboardRemove


last_message_time = None
router1 = Router()


spravka = [
    "Справка, что студент",
    "Справка-вызов",
    "Справка об обучении (периоде)",
    "Справка о размере стипендии",
    "Справка в военкомат",
]

grants = [
    "размер стипендии",
    "социальная стипендия",
    "информация о стипендии",
]
dekanat=[
"часы работы деканата",
"время работы деканата",
"связь с деканатом",
"телефон деканата"
]


@router1.callback_query(F.data == "table")
async def cmd_question(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "Возможность просмотра расписания появится в боте позднее\nЖдем и верим в моих разработчиков!💻")
    await callback.answer()


@router1.callback_query(F.data == "wi-fi")
async def cmd_wifi(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "Сеть: samgtu_emp пароль: ooChaThee4\n"
        "Сеть: samgtu_student пароль: cueX2CBH\n"
        "Сеть: samgtu_guest пароль:see8Zu6k")
    await callback.answer()


@router1.callback_query(F.data == "question")
async def cmd_question(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Bot_State.question)
    await callback.message.answer("Какой у тебя вопрос?")


@router1.callback_query(F.data == "exit")
async def cmd_exit(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Bot_State.exit)
    await callback.message.answer("До встречи! Если появятся вопросы, не стесняйся писать!✌")


@router1.message(Bot_State.question)
async def handle_question(message: types.Message, state: FSMContext):
    user_message = message.text.lower()
    if len(user_message) > 100:
        await message.answer("напиши, пожалуйста менее длинное сообщение")
        await state.set_state(Bot_State.question)
    if "справка" in user_message:
        await message.answer("Уточни, пожалуйста, какая справка:", reply_markup=make_row_keyboard(spravka))
        await state.set_state(Bot_State.direct_to_LLM)
    elif "стипендия" in user_message:
        await message.answer("Уточни, пожалуйста, какая информация о стипендии тебя интересует:",
                             reply_markup=make_row_keyboard(grants))
        await state.set_state(Bot_State.direct_to_LLM)
    elif "деканат" in user_message:
        await message.answer("Уточни, пожалуйста, какая информация о деканате тебя интересует:",
                             reply_markup=make_row_keyboard(dekanat))
        await state.set_state(Bot_State.direct_to_LLM)

    else:
        await process_general_question(message, state)


@router1.message(Bot_State.direct_to_LLM)
async def process_general_question(message: types.Message, state: FSMContext):
    global last_message_time
    current_time = datetime.now()
    time_limit = timedelta(seconds=10)

    if last_message_time is None or current_time - last_message_time > time_limit:
        await message.answer("Ваш запрос обрабатывается")
        answer = response.find_answer(message.text)
        await state.set_state(Bot_State.waiting_for_question)
        await message.answer(text=answer, reply_markup=ReplyKeyboardRemove())
        keyboard = create_keyboard()
        await message.answer("У тебя остались вопросы?", reply_markup=keyboard)
        last_message_time = datetime.now()
    else:

        await message.answer(f"Пожалуйста, подождите {10} секунд перед отправкой следующего сообщения.")


@router1.message(Bot_State.direct_to_LLM, F.text.in_(spravka + grants + dekanat))
async def handle_spravka_grants_decanat(message: types.Message, state: FSMContext):
    answer = response.find_answer(message.text.lower())
    await state.set_state(Bot_State.waiting_for_question)
    await message.answer(answer)
    keyboard = create_keyboard()
    await message.answer("У тебя остались вопросы?", reply_markup=keyboard)


def register_handlers(router: Router):
    router.include_router(router1)
