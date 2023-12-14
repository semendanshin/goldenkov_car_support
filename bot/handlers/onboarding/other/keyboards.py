from telegram import ReplyKeyboardMarkup, KeyboardButton

WRITE_TO_CHAT_BUTTON_TEXT = "Написать в чат"
CALL_BUTTON_TEXT = "Рассказать по телефону"


def get_other_question_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(WRITE_TO_CHAT_BUTTON_TEXT),
            ],
            [
                KeyboardButton(CALL_BUTTON_TEXT),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
