from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, ConversationHandler, filters
from telegram.ext import Application

from ..keyboards import CREDIT_LEASING_BUTTON_TEXT
from . import handlers
from . import keyboards
from . import enums


def register_handlers(app: Application):
    app.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(filters.Text((CREDIT_LEASING_BUTTON_TEXT, )), handlers.credit_leasing_start),
            ],
            states={
                enums.CreditLeasingConversionSteps.GET_SUBCATEGORY: [
                    MessageHandler(filters.Text((keyboards.CREDIT_BUTTON_TEXT, )), handlers.help_with_credit),
                    MessageHandler(filters.Text((keyboards.LEASING_BUTTON_TEXT, )), handlers.help_with_leasing),
                ],
                enums.CreditLeasingConversionSteps.GET_PHONE: [
                    MessageHandler(filters.Text(), handlers.set_phone_from_text),
                    MessageHandler(filters.CONTACT, handlers.set_phone_from_contact),
                ],
            },
            fallbacks=[
                CommandHandler('cancel', handlers.cancel),

            ],
            # name='credit_leasing',
            # persistent=True,
        )
    )