from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database.models import User
from .keyboards import get_credit_leasing_keyboard
from .enums import CreditLeasingConversionSteps
from ..handlers import update_user_phone_number, parse_russian_phone_number
from ..keyboards import get_main_keyboard, get_send_contact_keyboard


async def credit_leasing_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Кредит/лизинг 🏦",
        reply_markup=get_credit_leasing_keyboard(),
    )

    return CreditLeasingConversionSteps.GET_SUBCATEGORY


async def help_with_credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['credit_leasing'] = 'credit'

    if not context.database_user.phone_number:
        context.user_data['next_function'] = finish_credit
        await update.message.reply_text(
            "Введите номер телефона или отправьте контакт",
            reply_markup=get_send_contact_keyboard(),
        )
        return CreditLeasingConversionSteps.GET_PHONE

    return await finish_credit(update, context)


async def finish_credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ассистент подберет лучшие условия кредитования - "
        "задаст вам буквально несколько вопросов и сразу начнет работу.	",
        reply_markup=get_main_keyboard(),
    )
    return ConversationHandler.END


async def help_with_leasing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['credit_leasing'] = 'leasing'

    if not context.database_user.phone_number:
        context.user_data['next_function'] = finish_leasing
        await update.message.reply_text(
            "Введите номер телефона или отправьте контакт",
            reply_markup=get_send_contact_keyboard(),
        )
        return CreditLeasingConversionSteps.GET_PHONE

    return await finish_leasing(update, context)


async def finish_leasing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ассистент подберет лучшие условия лизинга - "
        "задаст вам буквально несколько вопросов и сразу начнет работу.	",
        reply_markup=get_main_keyboard(),
    )
    return ConversationHandler.END


async def set_phone_from_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.contact.phone_number
    database_user: User = context.database_user
    session = context.session
    await update_user_phone_number(session, database_user, phone)
    next_func = context.user_data.get('next_function')
    if next_func:
        return await next_func(update, context)
    return ConversationHandler.END


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
    next_func = context.user_data.get('next_function')
    if next_func:
        return await next_func(update, context)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отмена",
        reply_markup=get_main_keyboard(),
    )

    return ConversationHandler.END
