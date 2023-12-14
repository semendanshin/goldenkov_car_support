from telegram import ReplyKeyboardMarkup, KeyboardButton


CREDIT_BUTTON_TEXT = "Помочь с кредитом"
LEASING_BUTTON_TEXT = "Помочь с лизингом"


def get_credit_leasing_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(CREDIT_BUTTON_TEXT),
            ],
            [
                KeyboardButton(LEASING_BUTTON_TEXT),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
