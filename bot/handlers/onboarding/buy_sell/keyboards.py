from telegram import ReplyKeyboardMarkup, KeyboardButton


BUY_CAR_BUTTON_TEXT = "Хочу купить машину"
SELL_CAR_BUTTON_TEXT = "Хочу продать машину"


def get_buy_sell_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(BUY_CAR_BUTTON_TEXT),
            ],
            [
                KeyboardButton(SELL_CAR_BUTTON_TEXT),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
