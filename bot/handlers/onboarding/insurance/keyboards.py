from telegram import ReplyKeyboardMarkup, KeyboardButton


THE_BEST_INSURANCE_BUTTON_TEXT = "Подобрать лучшую страховку"
INSURANCE_QUESTION_BUTTON_TEXT = "Помочь в решении вопроса со страховой"


def get_insurance_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(THE_BEST_INSURANCE_BUTTON_TEXT),
            ],
            [
                KeyboardButton(INSURANCE_QUESTION_BUTTON_TEXT),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

