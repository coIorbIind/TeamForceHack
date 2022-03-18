from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Text, ForeignKey, PrimaryKeyConstraint, Table, create_engine

from config_classes import DBConfig
from config import load_config

db_config = load_config("db_cfg.cfg", DBConfig, '=')

engine = create_engine(db_config.conn_str)

Base = declarative_base()


class TopicUser(Base):  # Connects audience and user accounts
    __tablename__ = "topic_user"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id')),
    topic_id = Column(Integer(), ForeignKey('topics.id')),


class User(Base):
    """Represents user in database"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tgm_link = Column(Text)


class Message(Base):
    """Represents message from user in database"""
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    msg_text = Column(Text)
    sender_id = Column(Integer, ForeignKey('users.id'))
    topic_id = Column(Integer, ForeignKey('topics.id'))

    sender = relationship("User", uselist=False)
    topic = relationship("Topic", uselist=False)


class Topic(Base):
    """Represents message topic in database"""
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    name = Column(Text)

    author = relationship('User')
    addressees = relationship('TopicUser', backref="topic")


Base.metadata.create_all(engine)
