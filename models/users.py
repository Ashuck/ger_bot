from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base
from telebot.types import Message


class User(Base):
    __tablename__ = "users"

    tg_id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    request = relationship('UsersRequest')

    def __init__(self, tg_data: Message):
        self.tg_id = tg_data.from_user.id
        self.surname = tg_data.from_user.last_name
        self.name = tg_data.from_user.first_name

    def __repr__(self) -> str:
        return f"User: {self.name} {self.surname}"
    
    def check_state(self, bad_states):
        self_states = set(map(lambda x: x.state, self.request))
        other_states = set(map(lambda x: x.id, bad_states))
        if not self_states:
            return True
        else:
            return self_states.isdisjoint(other_states)