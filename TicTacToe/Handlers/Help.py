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

# Уровни сложности
DIFFICULTY_LEVELS = {
    "easy": "Легкий (случайные ходы)",
    "medium": "Средний (базовая логика)",
    "hard": "Сложный (непобедимый)"
}
current_difficulty = "medium"

def draw_board():
    board = ""
    for i in range(0, 9, 3):
        row = []
        for cell in game_board[i:i+3]:
            if cell == "X":
                row.append(X_CELL)
            elif cell == "O":
                row.append(O_CELL)
            else:
                row.append(EMPTY_CELL)
        board += "".join(row) + "\n"
    return board

def check_winner(board=None):
    if board is None:
        board = game_board
    
    # Проверка строк
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != " ":
            return board[i]
    
    # Проверка столбцов
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != " ":
            return board[i]
    
    # Проверка диагоналей
    if board[0] == board[4] == board[8] != " ":
        return board[0]
    if board[2] == board[4] == board[6] != " ":
        return board[2]
    
    # Проверка на ничью
    if " " not in board:
        return "D"
    
    return None

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    
    if winner == "O":
        return 10 - depth
    elif winner == "X":
        return depth - 10
    elif winner == "D":
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def bot_move():
    empty_cells = [i for i, cell in enumerate(game_board) if cell == " "]
    
    if current_difficulty == "easy":
        return random.choice(empty_cells) if empty_cells else None
    
    elif current_difficulty == "medium":
        # Проверка на победу бота
        for cell in empty_cells:
            game_board[cell] = "O"
            if check_winner() == "O":
                game_board[cell] = " "
                return cell
            game_board[cell] = " "
        
        # Блокировка игрока
        for cell in empty_cells:
            game_board[cell] = "X"
            if check_winner() == "X":
                game_board[cell] = " "
                return cell
            game_board[cell] = " "
        
        # Случайный ход
        return random.choice(empty_cells) if empty_cells else None
    
    elif current_difficulty == "hard":
        best_score = -float('inf')
        best_move = None
        
        for cell in empty_cells:
            game_board[cell] = "O"
            score = minimax(game_board, 0, False)
            game_board[cell] = " "
            
            if score > best_score:
                best_score = score
                best_move = cell
        
        return best_move

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
    
    if message.text.lower() in ["play", "играть", "начать"]:
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
            
            # Ход бота
            bot_cell = bot_move()
            if bot_cell is not None:
                game_board[bot_cell] = "O"
                
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