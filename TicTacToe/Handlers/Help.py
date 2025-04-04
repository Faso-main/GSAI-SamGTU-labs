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
player_score = 0
bot_score = 0
draws = 0

# Эмодзи для отрисовки доски
EMPTY_CELL = "⬜"
X_CELL = "❌"
O_CELL = "⭕"

# Уровни сложности (теперь только два)
DIFFICULTY_LEVELS = {
    "easy": "Легкий (случайные ходы)",
    "medium": "Средний (базовая логика)"
}
current_difficulty = "medium"

def draw_board():
    emoji_board = []
    for cell in game_board:
        if cell == "X":
            emoji_board.append(X_CELL)
        elif cell == "O":
            emoji_board.append(O_CELL)
        else:
            emoji_board.append(EMPTY_CELL)
    
    board = ""
    for i in range(0, 9, 3):
        board += f"{emoji_board[i]}{emoji_board[i+1]}{emoji_board[i+2]}\n"
    return board

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

def bot_move():
    empty_cells = [i for i, cell in enumerate(game_board) if cell == " "]
    
    # Легкий уровень - случайные ходы
    if current_difficulty == "easy":
        return random.choice(empty_cells) if empty_cells else None
    
    # Средний уровень
    # 1. Сначала проверяем, может ли бот выиграть
    for cell in empty_cells:
        game_board[cell] = "O"
        if check_winner() == "O":
            game_board[cell] = " "
            return cell
        game_board[cell] = " "
    
    # 2. Проверяем, может ли выиграть игрок, чтобы блокировать
    for cell in empty_cells:
        game_board[cell] = "X"
        if check_winner() == "X":
            game_board[cell] = " "
            return cell
        game_board[cell] = " "
    
    # 3. Случайный ход
    return random.choice(empty_cells) if empty_cells else None

async def animate_bot_move(message: Message, cell_index: int):
    temp_board = game_board.copy()
    for emoji in ["🔵", "⚪", "🔴"]:
        temp_board[cell_index] = emoji
        await message.edit_text(
            f"🤖 Бот думает ({DIFFICULTY_LEVELS[current_difficulty]})...\n\n{draw_animated_board(temp_board)}"
        )
        await asyncio.sleep(0.3)
    
    temp_board[cell_index] = "O"
    await message.edit_text(
        f"🤖 Бот походил!\n\n{draw_animated_board(temp_board)}"
    )
    await asyncio.sleep(0.5)

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

def create_game_keyboard():
    builder = ReplyKeyboardBuilder()
    for i in range(1, 10):
        builder.button(text=str(i))
    builder.button(text="❌ Закончить игру")
    builder.adjust(3, 3, 3, 1)
    return builder.as_markup(resize_keyboard=True)

def create_difficulty_keyboard():
    builder = ReplyKeyboardBuilder()
    for level in DIFFICULTY_LEVELS.values():
        builder.button(text=level)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

@router_help.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    global game_board, current_player, game_active, player_score, bot_score, draws, current_difficulty
    
    if message.text.lower() in ["play"]:
        await message.answer(
            "🎮 Выберите уровень сложности:",
            reply_markup=create_difficulty_keyboard()
        )
        await state.set_state(GameState.playing)
        return
    
    elif message.text in DIFFICULTY_LEVELS.values():
        for key, value in DIFFICULTY_LEVELS.items():
            if value == message.text:
                current_difficulty = key
                break
        
        game_board = [" "] * 9
        current_player = "X"
        game_active = True
        
        await message.answer(
            f"🎮 Игра началась!\n"
            f"Уровень: {DIFFICULTY_LEVELS[current_difficulty]}\n"
            f"Вы: {X_CELL} | Бот: {O_CELL}\n"
            f"Счет: {player_score}-{bot_score} (Ничьи: {draws})\n\n" + 
            draw_board(),
            reply_markup=create_game_keyboard()
        )
        return
    
    elif game_active and message.text.isdigit() and 1 <= int(message.text) <= 9:
        await state.set_state(GameState.waiting_for_move)
        cell_index = int(message.text) - 1
        
        if game_board[cell_index] == " ":
            game_board[cell_index] = "X"
            
            msg = await message.answer(
                f"Ваш ход...\n\n{draw_board()}",
                reply_markup=create_game_keyboard()
            )
            await asyncio.sleep(0.5)
            
            winner = check_winner()
            if winner == "X":
                player_score += 1
                await message.answer(
                    f"🎉 Вы победили!\nСчет: {player_score}-{bot_score}\n\n{draw_board()}",
                    reply_markup=ReplyKeyboardRemove()
                )
                game_active = False
                await state.clear()
                return
            elif winner == "D":
                draws += 1
                await message.answer(
                    f"🤝 Ничья!\nСчет: {player_score}-{bot_score}\n\n{draw_board()}",
                    reply_markup=ReplyKeyboardRemove()
                )
                game_active = False
                await state.clear()
                return
            
            bot_cell = bot_move()
            if bot_cell is not None:
                temp_msg = await message.answer(f"🤖 Бот думает...")
                await animate_bot_move(temp_msg, bot_cell)
                game_board[bot_cell] = "O"
                await temp_msg.delete()
                
                winner = check_winner()
                if winner == "O":
                    bot_score += 1
                    await message.answer(
                        f"😢 Бот победил!\nСчет: {player_score}-{bot_score}\n\n{draw_board()}",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    game_active = False
                    await state.clear()
                    return
                elif winner == "D":
                    draws += 1
                    await message.answer(
                        f"🤝 Ничья!\nСчет: {player_score}-{bot_score}\n\n{draw_board()}",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    game_active = False
                    await state.clear()
                    return
            
            await message.answer(
                f"Ваш ход (1-9):\n\n{draw_board()}",
                reply_markup=create_game_keyboard()
            )
            await state.set_state(GameState.playing)
        else:
            await message.answer("Клетка занята! Выберите другую.", reply_markup=create_game_keyboard())
            await state.set_state(GameState.playing)
    
    elif game_active and message.text == "❌ Закончить игру":
        game_active = False
        await message.answer(
            f"Игра завершена. Счет: {player_score}-{bot_score}",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
    
    else:
        await state.clear()
        await message.answer(
            "Напишите 'play' для начала игры",
            reply_markup=ReplyKeyboardRemove()
        )