from database import create_db, Session
from settings import SRO_TYPES

from models.users import User
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
    
    session.commit()
    session.close()