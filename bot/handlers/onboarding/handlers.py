from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import phonenumbers

from crud import user as user_crud

from database.models import User
from .enums import ConversationStepsEnum
from .static_text import GREETING
from .keyboards import (
    get_main_keyboard,
    get_send_contact_keyboard,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        GREETING,
        reply_markup=get_main_keyboard(),
    )

    if not context.database_user.phone_number:
        return 'SET_PHONE'

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отмена",
        reply_markup=get_main_keyboard(),
    )

    return ConversationHandler.END


async def start_set_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите номер телефона или отправьте контакт",
        reply_markup=get_send_contact_keyboard(),
    )

    return 'SET_PHONE'


async def set_phone_from_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        phone = parse_russian_phone_number(update.message.text)
    except ValueError:
        await update.message.reply_text(
            "Неверный формат номера телефона. Попробуйте еще раз",
            reply_markup=get_main_keyboard(),
        )
        return
    database_user: User = context.database_user
    session = context.session
    await update_user_phone_number(session, database_user, phone)
    return ConversationHandler.END


async def set_phone_from_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        phone = parse_russian_phone_number(update.message.contact.phone_number)
    except ValueError:
        await update.message.reply_text(
            "Неверный формат номера телефона. Попробуйте еще раз",
            reply_markup=get_main_keyboard(),
        )
        return
    database_user: User = context.database_user
    session = context.session
    await update_user_phone_number(session, database_user, phone)
    return ConversationHandler.END


async def update_user_phone_number(session: AsyncSession, user: User, phone_number: str) -> User:
    user.phone_number = phone_number
    await session.commit()
    return user


def parse_russian_phone_number(phone_number: str) -> str:
    phone = phonenumbers.parse(phone_number, "RU")
    if not phonenumbers.is_valid_number(phone):
        raise ValueError("Неверный формат номера телефона")
    return phonenumbers.format_number_for_mobile_dialing(phone, 'RU', True)
