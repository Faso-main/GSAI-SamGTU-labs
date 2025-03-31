import random
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Список из 200 философских вопросов
philosophical_questions = [
    "В чем смысл жизни?",
    "Существует ли свобода воли?",
]

# Состояния для игры
class GameState(StatesGroup):
    playing = State()
    waiting_for_move = State()

# Инициализация роутера
router_help = Router()

# Глобальные переменные для игры
game_board = [" "] * 9
current_player = "X"  # X - игрок, O - бот
game_active = False

# Функция для отрисовки доски
def draw_board():
    board = ""
    for i in range(0, 9, 3):
        board += f"{game_board[i]} | {game_board[i+1]} | {game_board[i+2]}\n"
        if i < 6:
            board += "---------\n"
    return board

# Функция проверки победы
def check_winner():
    # Проверка строк
    for i in range(0, 9, 3):
        if game_board[i] == game_board[i+1] == game_board[i+2] != " ":
            return game_board[i]
    
    # Проверка столбцов
    for i in range(3):
        if game_board[i] == game_board[i+3] == game_board[i+6] != " ":
            return game_board[i]
    
    # Проверка диагоналей
    if game_board[0] == game_board[4] == game_board[8] != " ":
        return game_board[0]
    if game_board[2] == game_board[4] == game_board[6] != " ":
        return game_board[2]
    
    # Проверка на ничью
    if " " not in game_board:
        return "D"
    
    return None

# Функция хода бота
def bot_move():
    empty_cells = [i for i, cell in enumerate(game_board) if cell == " "]
    if empty_cells:
        return random.choice(empty_cells)
    return None

# Обработчик текстовых сообщений
@router_help.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    global game_board, current_player, game_active
    
    # Создаем клавиатуру с номерами клеток (выносим это в начало, чтобы была доступна во всех ветках)
    builder = ReplyKeyboardBuilder()
    for i in range(1, 10):
        builder.button(text=str(i))
    builder.adjust(3, 3, 3)
    
    # Если пользователь хочет начать игру
    if message.text.lower() in ["крестики нолики", "играть", "x o", "xo", "х о", "хо"]:
        # Инициализация игры
        game_board = [" "] * 9
        current_player = "X"
        game_active = True
        
        await message.answer(
            "Игра в крестики-нолики началась!\n"
            "Вы играете за X. Выберите клетку (1-9):\n\n" + 
            draw_board(),
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(GameState.playing)
    
    # Если игра активна и введено число от 1 до 9
    elif game_active and message.text.isdigit() and 1 <= int(message.text) <= 9:
        await state.set_state(GameState.waiting_for_move)
        cell_index = int(message.text) - 1
        
        # Проверяем, свободна ли клетка
        if game_board[cell_index] == " ":
            # Ход игрока
            game_board[cell_index] = "X"
            
            # Проверяем результат после хода игрока
            winner = check_winner()
            if winner == "X":
                await message.answer(
                    f"{draw_board()}\nВы победили! 🎉",
                    reply_markup=ReplyKeyboardRemove()
                )
                game_active = False
                await state.clear()
                return
            elif winner == "D":
                await message.answer(
                    f"{draw_board()}\nНичья! 🤝",
                    reply_markup=ReplyKeyboardRemove()
                )
                game_active = False
                await state.clear()
                return
            
            # Ход бота
            bot_cell = bot_move()
            if bot_cell is not None:
                game_board[bot_cell] = "O"
                
                # Проверяем результат после хода бота
                winner = check_winner()
                if winner == "O":
                    await message.answer(
                        f"{draw_board()}\nБот победил! 😢",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    game_active = False
                    await state.clear()
                    return
                elif winner == "D":
                    await message.answer(
                        f"{draw_board()}\nНичья! 🤝",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    game_active = False
                    await state.clear()
                    return
            
            # Продолжаем игру
            await message.answer(
                f"Текущее состояние доски:\n\n{draw_board()}\nВаш ход (1-9):",
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
            await state.set_state(GameState.playing)
        else:
            await message.answer("Эта клетка уже занята! Выберите другую.")
            await state.set_state(GameState.playing)
    
    # Если игра не активна, отвечаем философским вопросом
    else:
        await state.clear()
        reply = random.choice(philosophical_questions)
        await message.answer(text=reply, reply_markup=ReplyKeyboardRemove())