from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id  = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    posts    = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "post"
    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    created = Column(TIMESTAMP)
    title   = Column(String)
    body    = Column(String)
    author  = relationship("User", back_populates="posts")
