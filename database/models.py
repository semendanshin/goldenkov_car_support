from sqlalchemy import Column, BigInteger, String, Enum, DateTime
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs

from datetime import datetime

from .enums import UserRolesEnum

Base = declarative_base()


class User(AsyncAttrs, Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(BigInteger, primary_key=True)
    username: Mapped[str] = Column(String, unique=True, nullable=True)
    first_name: Mapped[str] = Column(String, nullable=True)
    last_name: Mapped[str] = Column(String, nullable=True)
    role: Mapped[UserRolesEnum] = Column(Enum(UserRolesEnum), default=UserRolesEnum.USER)

    phone_number: Mapped[str] = Column(String, nullable=True)

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, first_name={self.first_name}, last_name={self.last_name})>'
