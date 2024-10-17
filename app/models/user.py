from app.database import db
from sqlalchemy.orm import relationship, Mapped, mapped_column
# from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.role import Role


# class User(db.Model):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String(255), nullable=False)
#     last_name = Column(String(255), nullable=False)
#     username = Column(String(255), nullable=False, unique=True)
#     email = Column(String(255), nullable=False, unique=True)
#     password = Column(String(255), nullable=False)

#     posts = relationship("app.models.post.Post", back_populates="user", cascade="all, delete-orphan")
#     comments = relationship("app.models.comment.Comment", back_populates="user", cascade="all, delete-orphan")

#     role_id = Column(Integer, ForeignKey("roles.id"), default=1)
#     role = relationship("Role", back_populates="users")
    
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
    
#     def __repr__(self):
#         return f"<User {self.id}|{self.username}>"



class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    username: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    
    role_id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"), default=1)
    role: Mapped[Role] = db.relationship("Role", back_populates='users')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<User {self.id}|{self.username}>"