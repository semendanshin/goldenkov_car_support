from telegram import ReplyKeyboardMarkup, KeyboardButton


SERVICE_REPAIR_BUTTON_TEXT = "Сервис/ремонт 🔧"
BUY_SELL_BUTTON_TEXT = "Купить/продать 🚗"
CREDIT_LEASING_BUTTON_TEXT = "Кредит/лизинг 🏦"
INSURANCE_BUTTON_TEXT = "Страхование 🛡"
OTHER_QUESTION_BUTTON_TEXT = "Другой вопрос ❓"


def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(SERVICE_REPAIR_BUTTON_TEXT),
                KeyboardButton(BUY_SELL_BUTTON_TEXT),
            ],
            [
                KeyboardButton(CREDIT_LEASING_BUTTON_TEXT),
                KeyboardButton(INSURANCE_BUTTON_TEXT),
            ],
            [
                KeyboardButton(OTHER_QUESTION_BUTTON_TEXT),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_send_contact_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("Отправить номер телефона", request_contact=True),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
