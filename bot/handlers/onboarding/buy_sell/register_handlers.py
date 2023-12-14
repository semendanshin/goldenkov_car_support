from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, CommandHandler, filters
from telegram.ext import Application

from bot.handlers.onboarding import keyboards as onboarding_keyboards

from . import handlers
from . import keyboards
from . import enums


def register_handlers(app: Application):
    app.add_handler(
        ConversationHandler(
            entry_points=[
               MessageHandler(filters.Text((onboarding_keyboards.BUY_SELL_BUTTON_TEXT, )), handlers.buy_sell_start),
            ],
            states={
                enums.BuySellConversationSteps.GET_SUBCATEGORY: [
                    MessageHandler(filters.Text(
                        [
                            keyboards.BUY_CAR_BUTTON_TEXT,
                        ]
                    ), handlers.want_to_buy_car),
                    MessageHandler(filters.Text(
                        [
                            keyboards.SELL_CAR_BUTTON_TEXT,
                        ]
                    ), handlers.want_to_sell_car),
                ],
                enums.BuySellConversationSteps.GET_CAR_REGISTRATION_NUMBER_OR_VIN: [
                    MessageHandler(filters.Text(), handlers.save_car_registration_number_or_vin),
                ],
                enums.BuySellConversationSteps.GET_CAR_MILEAGE: [
                    MessageHandler(filters.Text(), handlers.save_car_mileage),
                ],
                enums.BuySellConversationSteps.GET_CAR_BRAND_AND_MODEL: [
                    MessageHandler(filters.Text(), handlers.save_car_brand_and_model),
                ],
                enums.BuySellConversationSteps.GET_CLIENT_PHONE: [
                    MessageHandler(filters.Text(), handlers.save_client_phone_from_text),
                    MessageHandler(filters.CONTACT, handlers.save_client_phone_from_contact),
                ],
            },
            fallbacks=[
                CommandHandler('cancel', handlers.cancel),
            ],
            # name="buy_sell",
            # persistent=True,
        ),
    )
