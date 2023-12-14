from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from .keyboards import get_buy_sell_keyboard
from .enums import BuySellConversationSteps
from .schemas import BuyOrSellCarInfo
from ..handlers import parse_russian_phone_number, update_user_phone_number
from ..keyboards import get_send_contact_keyboard, get_main_keyboard

"""
BUY_CAR_BUTTON_TEXT = "Хочу купить машину"
SELL_CAR_BUTTON_TEXT = "Хочу продать машину"
"""


async def buy_sell_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Купить/продать 🚗",
        reply_markup=get_buy_sell_keyboard(),
    )
    return BuySellConversationSteps.GET_SUBCATEGORY


async def want_to_buy_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично! Теперь введите марку и модель машины, которую хотите купить",
    )

    context.user_data['buy_or_sell_car_info'] = BuyOrSellCarInfo(
        option='buy',
    )

    return BuySellConversationSteps.GET_CAR_BRAND_AND_MODEL


async def want_to_sell_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично! Теперь введите госномер или VIN машины, которую хотите продать",
    )

    context.user_data['buy_or_sell_car_info'] = BuyOrSellCarInfo(
        option='sell',
    )

    return BuySellConversationSteps.GET_CAR_REGISTRATION_NUMBER_OR_VIN


async def save_car_registration_number_or_vin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buy_or_sell_car_info: BuyOrSellCarInfo = context.user_data['buy_or_sell_car_info']

    data = update.message.text

    if len(data) > 9:
        buy_or_sell_car_info.vin = data
    else:
        buy_or_sell_car_info.registration_number = data

    await update.message.reply_text(
        "Введите пробег машины",
    )
    return BuySellConversationSteps.GET_CAR_MILEAGE


async def save_car_mileage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buy_or_sell_car_info: BuyOrSellCarInfo = context.user_data['buy_or_sell_car_info']
    buy_or_sell_car_info.mileage = update.message.text

    if not context.database_user.phone_number:
        await update.message.reply_text(
            "Введите номер телефона или отправьте контакт",
            reply_markup=get_send_contact_keyboard(),
        )
        return BuySellConversationSteps.GET_CLIENT_PHONE

    return await show_buy_sell_info(update, context)


async def save_car_brand_and_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buy_or_sell_car_info: BuyOrSellCarInfo = context.user_data['buy_or_sell_car_info']
    buy_or_sell_car_info.brand_and_model = update.message.text

    if not context.database_user.phone_number:
        await update.message.reply_text(
            "Введите номер телефона или отправьте контакт",
            reply_markup=get_send_contact_keyboard(),
        )
        return BuySellConversationSteps.GET_CLIENT_PHONE

    return await show_buy_sell_info(update, context)


async def show_buy_sell_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buy_or_sell_car_info: BuyOrSellCarInfo = context.user_data['buy_or_sell_car_info']

    if buy_or_sell_car_info.option == 'buy':
        await update.message.reply_text(
            f"Вы хотите купить машину <b>{buy_or_sell_car_info.brand_and_model}</b>. "
            f"Ваш номер телефона <b>{context.database_user.phone_number}</b>",
            reply_markup=get_main_keyboard(),
        )
    else:
        await update.message.reply_text(
            f"Вы хотите продать машину с {'госномером' if buy_or_sell_car_info.registration_number else 'VIN'} <b>{buy_or_sell_car_info.registration_number or buy_or_sell_car_info.vin}</b>"
            f" и пробегом <b>{buy_or_sell_car_info.mileage}</b> км. "
            f"Ваш номер телефона <b>{context.database_user.phone_number}</b>",
            reply_markup=get_main_keyboard(),
        )

    return ConversationHandler.END


async def save_client_phone_from_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text

    try:
        phone = parse_russian_phone_number(phone)
    except ValueError:
        await update.message.reply_text(
            "Неверный формат номера телефона. Попробуйте еще раз",
            reply_markup=get_main_keyboard(),
        )
        return

    await update_user_phone_number(context.session, context.database_user, phone)

    return await show_buy_sell_info(update, context)


async def save_client_phone_from_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.contact.phone_number

    try:
        phone = parse_russian_phone_number(phone)
    except ValueError:
        await update.message.reply_text(
            "Неверный формат номера телефона. Попробуйте еще раз",
            reply_markup=get_main_keyboard(),
        )
        return

    await update_user_phone_number(context.session, context.database_user, phone)

    return await show_buy_sell_info(update, context)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отмена",
        reply_markup=get_buy_sell_keyboard(),
    )

    return BuySellConversationSteps.GET_SUBCATEGORY

