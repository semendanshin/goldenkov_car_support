from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database.models import User
from .keyboards import get_service_repair_keyboard
from .enums import ServiceConversationSteps
from .schemas import ServiceRepairInfo
from ..handlers import parse_russian_phone_number, update_user_phone_number
from ..keyboards import get_send_contact_keyboard, get_main_keyboard

"""
THE_BEST_SERVICE_BUTTON_TEXT = "Посоветовать лучший сервис для твоего автомобиля"
THE_BEST_PRICE_BUTTON_TEXT = "Найти лучшую цену"
FIND_PARTS_BUTTON_TEXT = "Найти запчати"
SPEED_UP_REPAIR_BUTTON_TEXT = "Ускорить ремонт/обслуживание"
OTHER_SERVICE_REPAIR_BUTTON_TEXT = "Другой вопрос"
"""


async def service_repair_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Сервис/ремонт 🔧",
        reply_markup=get_service_repair_keyboard(),
    )

    return ServiceConversationSteps.GET_SUBCATEGORY


async def the_best_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Мы знаем все компании и подберем для вас лучший сервис."
        " Наши рекомендации основаны на отзывах наших клиентов и опыте личного взаимодействия. "
        "Найдем для вас персонального менеджера и дадим консультацию по любом вопросу.	"
    )

    await update.message.reply_text(
        "Введите гос или vin номер машины",
    )
    context.user_data["service_repair_info"] = ServiceRepairInfo(
        type="best",
    )
    return ServiceConversationSteps.GET_REGISTRATION_NUMBER_OR_VIN


async def get_registration_number_or_vin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.text
    repair_data: ServiceRepairInfo = context.user_data["service_repair_info"]

    print('alo')

    if len(data) > 9:
        repair_data.vin = data
    else:
        repair_data.registration_number = data

    await update.message.reply_text(
        "Введите пробег машины",
    )

    return ServiceConversationSteps.GET_MILEAGE


async def get_mileage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.text
    repair_data: ServiceRepairInfo = context.user_data["service_repair_info"]

    repair_data.mileage = data
    if repair_data.type == 'boost':
        return await finish_best_service(update, context)

    await update.message.reply_text(
        "Опишите коротко свой запрос (на пример: ТО, замена колодок, кузовной ремонт и т.д.)",
    )

    return ServiceConversationSteps.GET_PROBLEM_DESCRIPTION


async def get_problem_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.text
    repair_data: ServiceRepairInfo = context.user_data["service_repair_info"]

    repair_data.problem_description = data

    if not context.database_user.phone_number:
        context.user_data["next_function"] = finish_best_service
        await update.message.reply_text(
            "Введите номер телефона или отправьте контакт",
            reply_markup=get_send_contact_keyboard(),
        )
        return ServiceConversationSteps.GET_PHONE_NUMBER

    return await finish_best_service(update, context)


async def finish_best_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repair_data: ServiceRepairInfo = context.user_data["service_repair_info"]

    # TODO: send message to admin

    await update.message.reply_text(
        f"{repair_data.type} {repair_data.registration_number} {repair_data.vin} {repair_data.mileage} {repair_data.problem_description}",
    )

    await update.message.reply_text(
        f"Спасибо за ваш запрос. Мы свяжемся с вами в ближайшее время",
        reply_markup=get_main_keyboard(),
    )

    del context.user_data["service_repair_info"]

    return ConversationHandler.END


async def speed_up_repair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["service_repair_info"] = ServiceRepairInfo(
        type="boost",
    )
    await update.message.reply_text(
        "Так случается, что ремонт или обслуживание автомобиля не всегда проходит гладко. "
        "Мы поможем решить любую сложность или разобраться в непонятной ситуации. "
        "Буквально несколько вводных и ассистент подключится."
    )
    await update.message.reply_text(
        "Введите гос или vin номер машины",
    )
    return ServiceConversationSteps.GET_REGISTRATION_NUMBER_OR_VIN


async def find_parts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично! Теперь введите марку и модель машины, которую хотите отремонтировать",
    )
    return 'get_car_brand_and_model'


async def the_best_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично! Теперь введите марку и модель машины, которую хотите отремонтировать",
    )
    return 'get_car_brand_and_model'


async def other_service_repair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично! Теперь введите марку и модель машины, которую хотите отремонтировать",
    )
    return 'get_car_brand_and_model'


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отменено",
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
