from telegram import ReplyKeyboardMarkup, KeyboardButton


THE_BEST_SERVICE_BUTTON_TEXT = "Посоветовать лучший сервис для твоего автомобиля"
THE_BEST_PRICE_BUTTON_TEXT = "Найти лучшую цену"
FIND_PARTS_BUTTON_TEXT = "Найти запчати"
SPEED_UP_REPAIR_BUTTON_TEXT = "Ускорить ремонт/обслуживание"
OTHER_SERVICE_REPAIR_BUTTON_TEXT = "Другой вопрос"


def get_service_repair_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(THE_BEST_SERVICE_BUTTON_TEXT),
                KeyboardButton(THE_BEST_PRICE_BUTTON_TEXT),
            ],
            [
                KeyboardButton(FIND_PARTS_BUTTON_TEXT),
                KeyboardButton(SPEED_UP_REPAIR_BUTTON_TEXT),
            ],
            [
                KeyboardButton(OTHER_SERVICE_REPAIR_BUTTON_TEXT),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
