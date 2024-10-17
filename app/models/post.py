from app.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    body: Mapped[str] = mapped_column(db.String(1000))
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
    def __str__(self):
        return self.id

def __repr__(self):
        return f"<Post {self.id} by User {self.user_id} titled {self.title}>"