from typing import AsyncGenerator
from contextlib import asynccontextmanager

from config import config
from logging import getLogger
from bot import telegram_app

logger = getLogger(__name__)


def main():
    logger.info("Starting bot")
    telegram_app.run_polling()


if __name__ == '__main__':
    main()
