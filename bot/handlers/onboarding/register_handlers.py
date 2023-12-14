from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

from . import handlers
from .enums import ConversationStepsEnum
from .keyboards import (
    INSURANCE_BUTTON_TEXT,
    OTHER_QUESTION_BUTTON_TEXT,
    SERVICE_REPAIR_BUTTON_TEXT,
    BUY_SELL_BUTTON_TEXT,
    CREDIT_LEASING_BUTTON_TEXT,
)

from .buy_sell.register_handlers import register_handlers as buy_sell_register_handlers
from .credit.register_handlers import register_handlers as credit_register_handlers
from .insurance.register_handlers import register_handlers as insurance_register_handlers
from .service.register_handlers import register_handlers as service_register_handlers
from .other.register_handlers import register_handlers as other_register_handlers


def register_handlers(app: Application):
    # app.add_handler(
    #     ConversationHandler(
    #         entry_points=[
    #             MessageHandler(filters.Text((SERVICE_REPAIR_BUTTON_TEXT, )), handlers.service_repair),
    #             MessageHandler(filters.Text((BUY_SELL_BUTTON_TEXT, )), handlers.buy_sell),
    #             MessageHandler(filters.Text((CREDIT_LEASING_BUTTON_TEXT, )), handlers.credit_leasing),
    #             MessageHandler(filters.Text((INSURANCE_BUTTON_TEXT, )), handlers.insurance),
    #             MessageHandler(filters.Text((OTHER_QUESTION_BUTTON_TEXT, )), handlers.other_question),
    #         ],
    #         states={
    #             ConversationStepsEnum.CHOOSE_SUBCATEGORY_REPAIR: [
    #                 MessageHandler(filters.Text(
    #                     [
    #                         THE_BEST_SERVICE_BUTTON_TEXT,
    #                         THE_BEST_PRICE_BUTTON_TEXT,
    #                         FIND_PARTS_BUTTON_TEXT,
    #                         SPEED_UP_REPAIR_BUTTON_TEXT,
    #                         OTHER_SERVICE_REPAIR_BUTTON_TEXT,
    #                     ]
    #                 ), handlers.service_repair_save_subcategory),
    #             ],
    #             ConversationStepsEnum.CHOOSE_SUBCATEGORY_BUY_SELL: [
    #                 MessageHandler(filters.Text(
    #                     [
    #                         BUY_CAR_BUTTON_TEXT,
    #                         SELL_CAR_BUTTON_TEXT,
    #                     ]
    #                 ), handlers.buy_sell_save_subcategory),
    #             ],
    #             ConversationStepsEnum.CHOOSE_SUBCATEGORY_CREDIT_LEASING: [
    #                 MessageHandler(filters.Text(
    #                     [
    #                         CREDIT_BUTTON_TEXT,
    #                         LEASING_BUTTON_TEXT,
    #                     ]
    #                 ), handlers.credit_leasing_save_subcategory),
    #             ],
    #             ConversationStepsEnum.CHOOSE_SUBCATEGORY_INSURANCE: [
    #                 MessageHandler(filters.Text(
    #                     [
    #                         THE_BEST_INSURANCE_BUTTON_TEXT,
    #                         INSURANCE_QUESTION_BUTTON_TEXT,
    #                     ]
    #                 ), handlers.insurance_save_subcategory),
    #             ],
    #             ConversationStepsEnum.CHOOSE_SUBCATEGORY_OTHER_QUESTION: [
    #                 MessageHandler(filters.Text(
    #                     [
    #                         CALL_BUTTON_TEXT,
    #                         WRITE_TO_CHAT_BUTTON_TEXT,
    #                     ]
    #                 ), handlers.other_question_save_subcategory),
    #             ],
    #             ConversationStepsEnum.CHOOSE_CAR_REGISTRATION_NUMBER: [
    #                 MessageHandler(filters.Text(), handlers.car_registration_number_save),
    #             ],
    #         },
    #         fallbacks=[MessageHandler(filters.Text(('Отмена', )), handlers.cancel)],
    #         allow_reentry=True,
    #         persistent=True,
    #         name="onboarding",
    #     )
    # )

    buy_sell_register_handlers(app)
    credit_register_handlers(app)
    insurance_register_handlers(app)
    service_register_handlers(app)
    other_register_handlers(app)

    app.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler('set_phone', handlers.start_set_phone),
                CommandHandler('start', handlers.start),
            ],
            states={
                'SET_PHONE': [
                    MessageHandler(filters.Text(), handlers.set_phone_from_text),
                    MessageHandler(filters.CONTACT, handlers.set_phone_from_contact),
                ],
            },
            fallbacks=[MessageHandler(filters.Text(('Отмена', )), handlers.cancel)],
            allow_reentry=True,
            # persistent=True,
            # name="set_phone",
        )
    )
