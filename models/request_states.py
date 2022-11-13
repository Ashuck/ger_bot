from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dataclasses import dataclass

from database import Base


@dataclass
class RequestState(Base):
    __tablename__ = "request_states"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    to_do = Column(String)
    request = relationship("UsersRequest")

    def __repr__(self) -> str:
        return f"Request: {self.title} State: {self.to_do}"