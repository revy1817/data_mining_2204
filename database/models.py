from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Table

Base = declarative_base()

tag_post = Table(
    "tag_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(250), nullable=False, unique=False)
    url = Column(String, unique=True, nullable=False)
    first_img = Column(String, unique=False, nullable=True)
    create_date = Column(DateTime, unique=False, nullable=True)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False, unique=False)
    author = relationship("Author", backref="post")
    tags = relationship("Tag", secondary=tag_post, backref="post")
    comments = relationship("Comment", backref="post")


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True, nullable=False)
    name = Column(String(150), nullable=False)


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    url = Column(String, unique=True, nullable=False)


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False, unique=False)
    full_name = Column(String(250), nullable=False, unique=False)
    user_url = Column(String, nullable=False, unique=False)
    text = Column(Text, nullable=False, unique=False)
    parent_id = Column(Integer, ForeignKey("comment.id"), unique=False, nullable=True)
    parent = relationship("Comment", uselist=False, post_update=True)
