from app.database import db, Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
# from sqlalchemy import Column, Integer, String

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    users: Mapped[List["User"]] = db.relationship("User", back_populates="role")

# class Role(Base):
#     __tablename__ = "roles"
#     id = Column(Integer, primary_key=True)
#     role_name = Column(String(255), nullable=False, unique=True)
#     users = relationship("app.models.user.User", back_populates="role")