from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database.models import User
from .keyboards import get_other_question_keyboard
from .enums import OtherQuestionsConversationSteps
from .schemas import OtherQuestionInfo
from ..handlers import parse_russian_phone_number, update_user_phone_number
from ..keyboards import get_main_keyboard


async def other_question_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Другой вопрос ❓",
        reply_markup=get_other_question_keyboard()
    )

    return OtherQuestionsConversationSteps.GET_SUBCATEGORY


async def write_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['other_question_info'] = OtherQuestionInfo(
        type='write_to_chat',
    )
    if not context.database_user.phone_number:
        context.user_data['next_function'] = finish_other_questions
        await update.message.reply_text(
            "Пожалуйста, введите номер телефона или отправьте контакт",
        )
        return OtherQuestionsConversationSteps.GET_PHONE_NUMBER
    return await finish_other_questions(update, context)


async def call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['other_question_info'] = OtherQuestionInfo(
        type='call',
    )
    if not context.database_user.phone_number:
        context.user_data['next_function'] = finish_other_questions
        await update.message.reply_text(
            "Пожалуйста, введите номер телефона или отправьте контакт",
        )
        return OtherQuestionsConversationSteps.GET_PHONE_NUMBER
    return await finish_other_questions(update, context)


async def finish_other_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Спасибо за ваш запрос. Мы свяжемся с вами в ближайшее время",
        reply_markup=get_main_keyboard(),
    )
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


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отменено",
    )
    return ConversationHandler.END
