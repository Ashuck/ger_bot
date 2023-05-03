import telebot
import os
from telebot.types import Message, CallbackQuery

from database import DB_NAME, Session
from create_database import create_database

from models.users import User
from models.settings import Settings
from models.user_requests import UsersRequest
from models.request_states import RequestState

from keyboards import reg_board, abort_kbr, succes_kbr, city_kbr
from email_working import send_mail

if not os.path.exists(DB_NAME):
    create_database()

from settings import TOKEN, TEMPLATES, SRO_TYPES

bot = telebot.TeleBot(TOKEN.first().value, parse_mode="MARKDOWN")


def get_user(message, session) -> UsersRequest:
    user = session.query(User).get(message.from_user.id)

    if user is None:
        user = User(message)
        session.add(user)
        
        session.commit()
    return user


def change_state(title, new_to_do):
    return session.query(RequestState).filter_by(title=title, to_do=new_to_do)[0]


@bot.message_handler(commands=['start'])
def start_message(message: Message):
    user = get_user(message, session)
    bot.send_message(
        chat_id=message.chat.id, 
        text=TEMPLATES["hello"],
        reply_markup=reg_board
    )


@bot.message_handler(content_types='text', func=lambda x: x.text in SRO_TYPES)
def new_request_to_SRO(message: Message):

    user = get_user(message, session)

    if user.check_state(BAD_STATES):
        state = session.query(RequestState).filter_by(
            title=message.text,
            to_do="Ввод ФИО"
        )[0]
        request = UsersRequest()
        request.state = state.id
        request.user = user.tg_id
        session.add(request)
        session.commit()
        bot.send_message(
            chat_id=message.chat.id, 
            text=TEMPLATES["need_fio"],
        )
    else:
        bot.send_message(
            chat_id=message.chat.id, 
            text=TEMPLATES["need_close_request"],
            reply_markup=abort_kbr
        )


@bot.message_handler(content_types='text')
def process_text(message:Message):  
    user = get_user(message, session)
    if user.check_state(BAD_STATES):
        bot.send_message(
            chat_id=message.chat.id, 
            text=TEMPLATES["hello"],
            reply_markup=reg_board
        )
        return None

    request: UsersRequest = user.request[-1]
    state = session.query(RequestState).get(request.state)

    if state.to_do == "Ввод ФИО":
        request.full_name = message.text
        request.state = change_state(state.title, "Ввод организации").id
        text = TEMPLATES["need_org"]
    
    elif state.to_do == "Ввод организации":
        request.organization = message.text
        request.state = change_state(state.title, "Ввод почты").id
        text = TEMPLATES["need_email"]
        
    elif state.to_do == "Ввод почты":
        request.email = message.text
        request.state = change_state(state.title, "Ввод телефона").id
        text = TEMPLATES["need_phone"]

    elif state.to_do == "Ввод телефона":
        request.phone = message.text
        if state.title == "СРО в области строительства":
            request.state = change_state(state.title, "Ввод региона").id
            text = TEMPLATES["need_region"]
            bot.send_message(
                chat_id=message.chat.id, 
                text=text,
                reply_markup=city_kbr
            )
            session.commit()
            return None

        else:
            request.region = "Не указывается"
            request.state = change_state(state.title, "Подтверждение данных").id
            text = TEMPLATES["need_check_projects"].format(
                    fio=request.full_name,
                    email=request.email,
                    phone=request.phone,
                    org=request.organization
                )
            bot.send_message(
                chat_id=message.chat.id, 
                text=text,
                reply_markup=succes_kbr
            )
            session.commit()
            return None

    elif state.to_do == "Ввод региона":
        request.region = message.text
        request.state = change_state(state.title, "Подтверждение данных").id
        text = TEMPLATES["need_check_builders"].format(
            fio=request.full_name,
            email=request.email,
            phone=request.phone,
            region=request.region,
            org=request.organization
        )

        bot.send_message(
            chat_id=message.chat.id, 
            text=text,
            reply_markup=succes_kbr
        )
        session.commit()
        return None
    elif state.to_do == "Подтверждение данных":
        text = TEMPLATES["need_check_builders"].format(
            fio=request.full_name,
            email=request.email,
            phone=request.phone,
            region=request.region,
            org=request.organization
        )
        bot.send_message(
            chat_id=message.chat.id, 
            text=text,
            reply_markup=succes_kbr
        )
        session.commit()
        return None
    
    else:
        return None

    bot.send_message(
        chat_id=message.chat.id, 
        text=text,
    )
    session.commit()


@bot.callback_query_handler(func=lambda call: call.data == "success")
def success_informatiom(message: CallbackQuery):
    user = get_user(message, session)
    request: UsersRequest = user.request[-1]
    state = session.query(RequestState).get(request.state)
    if state.to_do == "Подтверждение данных":
        request.state = change_state(state.title, "Выполнена").id
        text = TEMPLATES["success"].format(purpes=state.title)
        session.commit()

        if state.title == "СРО в области строительства" and request.region != "Иваново":
            recipient = session.query(Settings).get("email_other").value

        elif state.title == "СРО в области проектирования":
            recipient = session.query(Settings).get("email_ivanovo").value

        mail_text = TEMPLATES["mail_text"].format(
            sro=state.title,
            fio=request.full_name,
            email=request.email,
            phone=request.phone,
            region=request.region,
            org=request.organization
        )

        send_mail(
            text=mail_text,
            recipient=recipient,
            user=session.query(Settings).get("email_sender").value,
            password=session.query(Settings).get("email_sender_pass").value
        )
    else:
        text = TEMPLATES["nothing_to_success"]
    
    bot.send_message(
        chat_id=message.message.chat.id, 
        text=text,
    )


@bot.callback_query_handler(func=lambda call: call.data == "resume")
def resume_request(message: CallbackQuery):
    user = get_user(message, session)
    request: UsersRequest = user.request[-1]
    state = session.query(RequestState).get(request.state)
    kb = []
    if user.check_state(BAD_STATES):
        text=TEMPLATES["hello"]

    elif state.to_do == "Ввод ФИО":
        text=TEMPLATES["need_fio"]
    
    elif state.to_do == "Ввод организации":
        text = TEMPLATES["need_org"]
        
    elif state.to_do == "Ввод почты":
        text = TEMPLATES["need_email"]
        
    elif state.to_do == "Ввод телефона":
        text = TEMPLATES["need_phone"]

    elif state.to_do == "Ввод региона":
        text = TEMPLATES["need_region"]
    elif state.to_do == "Подтверждение данных":
        text = TEMPLATES["need_check_builders"].format(
            fio=request.full_name,
            email=request.email,
            phone=request.phone,
            region=request.region,
            org=request.organization
        )
        kb = succes_kbr
        
    bot.send_message(
        chat_id=message.message.chat.id, 
        text=text,
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call: call.data in ("drop", "cancel"))
def success_informatiom(message: CallbackQuery):
    user = get_user(message, session)
    request: UsersRequest = user.request[-1]
    state = session.query(RequestState).get(request.state)
    if state.to_do == "Подтверждение данных" or message.data == "cancel":
        request.state = change_state(state.title, "Отменена").id
        text = TEMPLATES["drop"]
        session.commit()
        bot.send_message(
            chat_id=message.message.chat.id, 
            text=text,
            reply_markup=reg_board
        )
    else:
        bot.send_message(
            chat_id=message.message.chat.id, 
            text=TEMPLATES["nothing_to_drop"],
        )

if __name__ == "__main__":
     
    session = Session()
    BAD_STATES = session.query(RequestState).filter(
        ~RequestState.to_do.in_(["Отменена", "Выполнена"])
    )

    bot.infinity_polling()