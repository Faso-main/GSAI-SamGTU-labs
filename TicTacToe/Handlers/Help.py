import random
import asyncio
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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

# Эмодзи для отрисовки доски
EMPTY_CELL = "⬜"
X_CELL = "❌"
O_CELL = "⭕"
BOARD_LINE = "➖"

# Функция для отрисовки доски с эмодзи
def draw_board():
    # Преобразуем игровое поле в эмодзи
    emoji_board = []
    for cell in game_board:
        if cell == "X":
            emoji_board.append(X_CELL)
        elif cell == "O":
            emoji_board.append(O_CELL)
        else:
            emoji_board.append(EMPTY_CELL)
    
    # Собираем доску из эмодзи
    board = ""
    for i in range(0, 9, 3):
        board += f"{emoji_board[i]}{emoji_board[i+1]}{emoji_board[i+2]}\n"
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
    if empty_cells: return random.choice(empty_cells)
    return None

# Анимация хода бота
async def animate_bot_move(message: Message, cell_index: int):
    # Временно показываем анимацию
    temp_board = game_board.copy()
    for emoji in ["🔵", "⚪", "🔴"]:
        temp_board[cell_index] = emoji
        await message.edit_text(
            f"Бот думает...\n\n{draw_animated_board(temp_board)}",
            reply_markup=message.reply_markup
        )
        await asyncio.sleep(0.3)
    
    # Возвращаем оригинальное значение
    temp_board[cell_index] = "O"
    await message.edit_text(
        f"Бот походил!\n\n{draw_animated_board(temp_board)}",
        reply_markup=message.reply_markup
    )
    await asyncio.sleep(0.5)

# Функция для отрисовки анимированной доски
def draw_animated_board(board):
    emoji_board = []
    for cell in board:
        if cell == "X":
            emoji_board.append(X_CELL)
        elif cell == "O":
            emoji_board.append(O_CELL)
        elif cell in ["🔵", "⚪", "🔴"]:
            emoji_board.append(cell)
        else:
            emoji_board.append(EMPTY_CELL)
    
    animated_board = ""
    for i in range(0, 9, 3):
        animated_board += f"{emoji_board[i]}{emoji_board[i+1]}{emoji_board[i+2]}\n"
    return animated_board

# Обработчик текстовых сообщений
@router_help.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    global game_board, current_player, game_active
    
    # Создаем клавиатуру с номерами клеток
    builder = ReplyKeyboardBuilder()
    for i in range(1, 10):
        builder.button(text=str(i))
    builder.adjust(3, 3, 3)
    reply_markup = builder.as_markup(resize_keyboard=True)
    
    # Если пользователь хочет начать игру
    if message.text.lower() in ["крестики нолики", "играть", "x o", "xo", "х о", "хо"]:
        # Инициализация игры
        game_board = [" "] * 9
        current_player = "X"
        game_active = True
        
        # Для первого сообщения используем answer с reply_markup
        await message.answer(
            "🎮 Игра в крестики-нолики началась!\n"
            f"Вы играете за {X_CELL}\n\n" + 
            draw_board(),
            reply_markup=reply_markup
        )
        await state.set_state(GameState.playing)
        return
    
    # Если игра активна и введено число от 1 до 9
    elif game_active and message.text.isdigit() and 1 <= int(message.text) <= 9:
        await state.set_state(GameState.waiting_for_move)
        cell_index = int(message.text) - 1
        
        # Проверяем, свободна ли клетка
        if game_board[cell_index] == " ":
            # Ход игрока
            game_board[cell_index] = "X"
            
            # Для сообщений с клавиатурой используем answer, а не edit_text
            msg = await message.answer(
                f"Ваш ход...\n\n{draw_board()}",
                reply_markup=reply_markup
            )
            await asyncio.sleep(0.5)
            
            # Проверяем результат после хода игрока
            winner = check_winner()
            if winner == "X":
                await message.answer(
                    f"🎉 Поздравляю! Вы победили!\n\n{draw_board()}",
                    reply_markup=ReplyKeyboardRemove()
                )
                game_active = False
                await state.clear()
                return
            elif winner == "D":
                await message.answer(
                    f"🤝 Ничья!\n\n{draw_board()}",
                    reply_markup=ReplyKeyboardRemove()
                )
                game_active = False
                await state.clear()
                return
            
            # Ход бота
            bot_cell = bot_move()
            if bot_cell is not None:
                # Для анимации используем новое сообщение
                temp_msg = await message.answer("Бот думает...")
                await animate_bot_move(temp_msg, bot_cell)
                game_board[bot_cell] = "O"
                await temp_msg.delete()
                
                # Проверяем результат после хода бота
                winner = check_winner()
                if winner == "O":
                    await message.answer(
                        f"😢 Бот победил!\n\n{draw_board()}",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    game_active = False
                    await state.clear()
                    return
                elif winner == "D":
                    await message.answer(
                        f"🤝 Ничья!\n\n{draw_board()}",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    game_active = False
                    await state.clear()
                    return
            
            # Продолжаем игру - отправляем новое сообщение с клавиатурой
            await message.answer(
                f"Ваш ход (1-9):\n\n{draw_board()}",
                reply_markup=reply_markup
            )
            await state.set_state(GameState.playing)
        else:
            await message.answer("Эта клетка уже занята! Выберите другую.", reply_markup=reply_markup)
            await state.set_state(GameState.playing)
    
    # Если игра не активна, отвечаем философским вопросом
    else:
        await state.clear()
        await message.answer(text='Ответ', reply_markup=ReplyKeyboardRemove())

async def animate_bot_move(message: Message, cell_index: int):
    # Временно показываем анимацию в новом сообщении
    temp_board = game_board.copy()
    for emoji in ["🔵", "⚪", "🔴"]:
        temp_board[cell_index] = emoji
        await message.edit_text(
            f"Бот думает...\n\n{draw_animated_board(temp_board)}"
        )
        await asyncio.sleep(0.3)
    
    # Финальное состояние анимации
    temp_board[cell_index] = "O"
    await message.edit_text(
        f"Бот походил!\n\n{draw_animated_board(temp_board)}"
    )
    await asyncio.sleep(0.5)