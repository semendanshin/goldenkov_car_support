from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database.models import User
from .keyboards import get_insurance_keyboard
from .enums import InsuranceConversationSteps
from .schemas import InsuranceInfo
from ..handlers import parse_russian_phone_number, update_user_phone_number
from ..keyboards import get_main_keyboard


async def insurance_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Страхование 🛡",
        reply_markup=get_insurance_keyboard(),
    )

    return InsuranceConversationSteps.GET_SUBCATEGORY


async def choose_the_best_insurance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.database_user.phone_number:
        context.user_data['next_function'] = finish_best_insurance
        await update.message.reply_text(
            "Пожалуйста, введите номер телефона или отправьте контакт",
            reply_markup=get_main_keyboard(),
        )
        return InsuranceConversationSteps.GET_PHONE_NUMBER

    return await finish_best_insurance(update, context)


async def finish_best_insurance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ассистент подберет лучшие условия страхования. Задаст вам буквально несколько вопросов и сразу начнет работу.",
        reply_markup=get_main_keyboard(),
    )
    return ConversationHandler.END


async def help_with_insurance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите госномер или vin-номер автомобиля, чтобы мы могли помочь вам с решением вопроса.",
    )

    return InsuranceConversationSteps.GET_REGISTRATION_NUMBER_OR_VIN


async def save_registration_number_or_vin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.text
    insurance_info = InsuranceInfo()

    if len(data) > 9:
        insurance_info.vin = data
    else:
        insurance_info.registration_number = data

    context.user_data['insurance_info'] = insurance_info

    if not context.database_user.phone_number:
        context.user_data['next_function'] = finish_help_with_insurance
        await update.message.reply_text(
            "Пожалуйста, введите номер телефона или отправьте контакт",
            reply_markup=get_main_keyboard(),
        )
        return InsuranceConversationSteps.GET_PHONE_NUMBER

    return await finish_help_with_insurance(update, context)


async def finish_help_with_insurance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    insurance_info: InsuranceInfo = context.user_data['insurance_info']

    await update.message.reply_text(
        f"Вы ввели {'vin' if insurance_info.vin else 'госномер'}: {insurance_info.vin or insurance_info.registration_number}."
    )

    await update.message.reply_text(
        "Так случается, что взаимодействие со страховой компанией или ремонт по страховке не всегда проходят гладко. "
        "Мы поможем решить любую сложность или разобраться в непонятной ситуации. "
        "Буквально несколько вводных и ассистент подключится.",
        reply_markup=get_main_keyboard(),
    )

    return ConversationHandler.END


async def get_phone_number_from_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def get_phone_number_from_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
