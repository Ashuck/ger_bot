from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from database import Base


class UsersRequest(Base):
    __tablename__ = "user_requests"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    organization = Column(String)
    email = Column(String)
    phone = Column(String)
    region = Column(String)
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, onupdate=func.now())
    state = Column(Integer, ForeignKey("request_states.id"))
    user = Column(Integer, ForeignKey("users.tg_id"))

    def __repr__(self) -> str:
        return f"{self.state} from {self.user}"