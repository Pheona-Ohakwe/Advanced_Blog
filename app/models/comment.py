from app.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(db.String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    
    def __str__(self):
        return self.id

    def __repr__(self):
        return f"<Comment {self.id} by User {self.user_id} on Post {self.post_id}>"