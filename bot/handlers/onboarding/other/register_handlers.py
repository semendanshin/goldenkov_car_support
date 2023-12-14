from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

from . import handlers
from .enums import OtherQuestionsConversationSteps
from .keyboards import (
    WRITE_TO_CHAT_BUTTON_TEXT,
    CALL_BUTTON_TEXT,
)
from ..keyboards import (
    OTHER_QUESTION_BUTTON_TEXT,
)


def register_handlers(app: Application):
    app.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(filters.Text((OTHER_QUESTION_BUTTON_TEXT, )), handlers.other_question_start),
            ],
            states={
                OtherQuestionsConversationSteps.GET_SUBCATEGORY: [
                    MessageHandler(filters.Text((WRITE_TO_CHAT_BUTTON_TEXT, )), handlers.write_to_chat),
                    MessageHandler(filters.Text((CALL_BUTTON_TEXT, )), handlers.call),
                ],
            },
            fallbacks=[
                CommandHandler('cancel', handlers.cancel)
            ],
            # name="other_questions",
            # persistent=True,

        )
    )