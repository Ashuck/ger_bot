from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from settings import SRO_TYPES, CITIES


reg_board = ReplyKeyboardMarkup(True)
reg_board.add(
    KeyboardButton(SRO_TYPES[0])
)

reg_board.add(
    KeyboardButton(SRO_TYPES[1])
)

abort_kbr = InlineKeyboardMarkup()
abort_kbr.add(
    InlineKeyboardButton("Продолжить", callback_data="resume")
)
abort_kbr.add(
    InlineKeyboardButton("Отменить", callback_data="cancel")
)

succes_kbr = InlineKeyboardMarkup()
succes_kbr.add(
    InlineKeyboardButton("Подтвержаю", callback_data="success")
)
succes_kbr.add(
    InlineKeyboardButton("Нет", callback_data="drop")
)

city_kbr = ReplyKeyboardMarkup(True)
for cities_list in CITIES:
    city_kbr.add(*[KeyboardButton(city) for city in cities_list])