from telegram.ext import Application, PersistenceInput, PicklePersistence
from telegram.ext import Defaults

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from database import engine

from bot.middlewares import SessionMiddleware, UserMiddleware, Middleware

from bot.handlers.onboarding import register_handlers as register_start_handlers

from config import config

from logging.handlers import RotatingFileHandler
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        RotatingFileHandler("logs/bot.log", maxBytes=200000, backupCount=5),
        logging.StreamHandler(),
    ]
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def get_telegram_app() -> Application:
    async def post_init(application: Application) -> None:
        await application.bot.set_my_commands(
            [
                ('start', 'Запустить бота'),
                ('cancel', 'Отменить'),
            ]
        )

    session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    middleware = Middleware(
        [
            SessionMiddleware(session_maker),
            UserMiddleware(),
        ],
    )

    token = config.bot_token.get_secret_value()

    # persistence_input = PersistenceInput(bot_data=True, user_data=True, chat_data=False, callback_data=False)
    # persistence = PicklePersistence('bot/persistence.pickle', store_data=persistence_input, update_interval=1)
    defaults = Defaults(disable_web_page_preview=True, parse_mode='HTML')
    # app = Application.builder().token(token).persistence(persistence).post_init(post_init).defaults(defaults).build()
    app = Application.builder().token(token).post_init(post_init).defaults(defaults).build()

    middleware.attach_to_application(app)

    register_start_handlers(app)

    # app.add_error_handler(send_stacktrace_to_tg_chat)

    return app


if __name__ == '__main__':
    app = get_telegram_app()
    app.run_polling()
