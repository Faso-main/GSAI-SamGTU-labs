import asyncio, os, logging
from aiogram import Bot, Dispatcher
from Handlers import Dispatch, Help
from Handlers.Encoded import arato_key

logging.basicConfig(level=logging.INFO, format="%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = logging.getLogger()

token = os.getenv("TELEGRAM_BOT_TOKEN", arato_key)
bot = Bot(token)
dp = Dispatcher()


async def main() -> None:
    try:
        dp.include_router(Dispatch.router3)
        dp.include_router(Help.router2)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e: logging.error(f"Error in main: {e}")
    finally: await bot.close()


if __name__ == '__main__':
    print(f'Digital assistant is running.............')
    try: asyncio.run(main())
    except KeyboardInterrupt: logging.info("Bot stopped by user.")
    except Exception as e: logging.error(f"Error: {e}")


