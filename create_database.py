from database import create_db, Session
from settings import SRO_TYPES

from models.users import User
from models.settings import Settings
from models.user_requests import UsersRequest
from models.request_states import RequestState

from itertools import product


def create_database():
    create_db()

    session = Session()

    state_todo = [
        "Ввод региона",
        "Ввод организации",
        "Ввод ФИО",
        "Ввод почты",
        "Ввод телефона",
        "Подтверждение данных",
        "Выполнена",
        "Отменена"
    ]

    session.add_all(
        map(
            lambda state: RequestState(title=state[0], to_do=state[1]), 
            product(SRO_TYPES, state_todo)
    ))

    session.add(
        Settings(
            name="BOT_TOKEN",
            value=input("Укажите токен бота: ")
        )
    )
    session.add(
        Settings(
            name="email_ivanovo",
            value=input("Укажите email для 'области проектирования' и 'области строительства в Иваново': ")
        )
    )
    session.add(
        Settings(
            name="email_other",
            value=input("Укажите email для 'области строительства не в Иваново': ")
        )
    )
    session.add(
        Settings(
            name="email_sender",
            value=input("Укажите email для отправки заявок: ")
        )
    )
    session.add(
        Settings(
            name="email_sender_pass",
            value=input("Укажите пароль для email: ")
        )
    )
    
    session.commit()
    session.close()

if __name__ == "__main__":
    create_database()