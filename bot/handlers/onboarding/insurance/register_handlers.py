from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

from ..keyboards import INSURANCE_BUTTON_TEXT
from .enums import InsuranceConversationSteps
from . import handlers
from . import keyboards


def register_handlers(app: Application):
    app.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(filters.Text((INSURANCE_BUTTON_TEXT, )), handlers.insurance_start),
            ],
            states={
                InsuranceConversationSteps.GET_SUBCATEGORY: [
                    MessageHandler(filters.Text((keyboards.THE_BEST_INSURANCE_BUTTON_TEXT, )), handlers.choose_the_best_insurance),
                    MessageHandler(filters.Text((keyboards.INSURANCE_QUESTION_BUTTON_TEXT, )), handlers.help_with_insurance),
                ],
                InsuranceConversationSteps.GET_PHONE_NUMBER: [
                    MessageHandler(filters.Text(), handlers.get_phone_number_from_text),
                    MessageHandler(filters.CONTACT, handlers.get_phone_number_from_contact),
                ],
                InsuranceConversationSteps.GET_REGISTRATION_NUMBER_OR_VIN: [
                    MessageHandler(filters.Text(), handlers.save_registration_number_or_vin),
                ],
            },
            fallbacks=[MessageHandler(filters.Text(('Отмена', )), handlers.cancel)],
            # persistent=True,
            # name="insurance",
        )
    )
