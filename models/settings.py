from sqlalchemy import Column, Integer, String

from database import Base


class Settings(Base):
    __tablename__ = "settings"

    # id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    value = Column(String)

    def __repr__(self) -> str:
        return self.name