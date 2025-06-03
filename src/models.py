from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import Enum as SqlEnum
from enum import Enum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            # do not serialize the password, it's a security breach
        }

class Post(db.Model):
    __tablename__ = 'POST'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)
    post_text: Mapped[str] = mapped_column(String(2200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="posts")
    media: Mapped[list["Media"]] = relationship("Media", back_populates="post")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")

class Follower(db.Model):
    __tablename__ = 'Follower'
    user_from_id: Mapped[int] = mapped_column(ForeignKey('User.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('User.id'), primary_key=True)

    user_from: Mapped["User"] = relationship("User", foreign_keys=[user_from_id], backref="followers_sent")
    user_to: Mapped["User"] = relationship("User", foreign_keys=[user_to_id], backref="followers_received")

class Media(db.Model):
    __tablename__ = 'Media'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    media_type: Mapped[MediaType] = mapped_column(SqlEnum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('POST.id'), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="media")

class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    OTHER = "other"

class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(1000))
    author_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('POST.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
