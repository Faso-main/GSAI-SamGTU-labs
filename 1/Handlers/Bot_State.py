from aiogram.fsm.state import State,StatesGroup


class Bot_State(StatesGroup):
    waiting_for_question = State()
    exit = State()
    question = State()
    direct_to_LLM=State()
