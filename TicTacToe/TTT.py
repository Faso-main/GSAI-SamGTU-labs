import asyncio, os, logging
from aiogram import Bot, Dispatcher
from Handlers import Dispatch, Help

logging.basicConfig(level=logging.INFO, format="%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = logging.getLogger()

token = os.getenv("TELEGRAM_BOT_TOKEN", '7752465950:AAEoaAZMckY75p10uLTqcRaZ8Bxz6opaAkA')
bot = Bot(token)
dp = Dispatcher()


async def main() -> None:
    try:
        dp.include_router(Dispatch.router_dispatch)
        dp.include_router(Help.router_help)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e: logging.error(f"Error in main: {e}")
    finally: await bot.close()


if __name__ == '__main__':
    print(f'TicTacToeBot is running.............')
    try: asyncio.run(main())
    except KeyboardInterrupt: logging.info("Bot stopped by user.")
    except Exception as e: logging.error(f"Error: {e}")


