from telegram.ext import MessageHandler, filters, ConversationHandler, CommandHandler
from telegram.ext import Application

from . import handlers
from . import keyboards
from . import enums

from ..keyboards import SERVICE_REPAIR_BUTTON_TEXT


def register_handlers(app: Application):
    app.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(filters.Text((SERVICE_REPAIR_BUTTON_TEXT, )), handlers.service_repair_start),
            ],
            states={
                enums.ServiceConversationSteps.GET_SUBCATEGORY: [
                    MessageHandler(filters.Text((keyboards.THE_BEST_SERVICE_BUTTON_TEXT, )), handlers.the_best_service),
                    MessageHandler(filters.Text((keyboards.SPEED_UP_REPAIR_BUTTON_TEXT, )), handlers.speed_up_repair),
                ],
                enums.ServiceConversationSteps.GET_REGISTRATION_NUMBER_OR_VIN: [
                    MessageHandler(filters.Text(), handlers.get_registration_number_or_vin),
                ],
                enums.ServiceConversationSteps.GET_MILEAGE: [
                    MessageHandler(filters.Text(), handlers.get_mileage),
                ],
                enums.ServiceConversationSteps.GET_PROBLEM_DESCRIPTION: [
                    MessageHandler(filters.Text(), handlers.get_problem_description),
                ],
                enums.ServiceConversationSteps.GET_PHONE_NUMBER: [
                    MessageHandler(filters.Text(), handlers.get_phone_number_from_text),
                    MessageHandler(filters.CONTACT, handlers.get_phone_number_from_contact),
                ],
            },
            fallbacks=[
                CommandHandler('cancel', handlers.cancel)
            ],
            # name="service_repair",
            # persistent=True,

        )
    )
