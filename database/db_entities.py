from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Text, ForeignKey, PrimaryKeyConstraint, Table, create_engine

from config_classes import DBConfig
from config import load_config

db_config = load_config("database/db_cfg.cfg", DBConfig, '=')

engine = create_engine(db_config.conn_str)

Base = declarative_base()


topic_user = Table(
    'topic_user',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('topic_id', ForeignKey('topics.id'), primary_key=True),
    #PrimaryKeyConstraint()

)


class User(Base):
    """Represents user in database"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tgm_link = Column(Text)
    chat_id = Column(Text)

    topics = relationship('Topic')
    topics_listener = relationship('Topic', secondary=topic_user, backref='topics_listener')

    def __repr__(self):
        return f"User(id={self.id}, tgm_link={self.tgm_link}, topics={self.topics})"

    def __eq__(self, other: 'User'):
        return self.tgm_link == other.tgm_link


class Message(Base):
    """Represents message from user in database"""
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    msg_text = Column(Text)
    sender_id = Column(Integer, ForeignKey('users.id'))
    topic_id = Column(Integer, ForeignKey('topics.id'))

    sender = relationship("User", uselist=False)
    topic = relationship("Topic", uselist=False)

    def __repr__(self):
        return f"Message(id={self.id}, msg_text={self.msg_text}, sender={self.sender})," \
               f"topic={self.topic})"


class Topic(Base):
    """Represents message topic in database"""
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    name = Column(Text)
    text = Column(Text)

    author = relationship('User', overlaps='topics', uselist=False)
    addressees = relationship('User', secondary=topic_user, backref='addresses')
    messages = relationship('Message', overlaps='topics')

    def __repr__(self):
        return f"Topic(id={self.id}, author_id={self.author_id}, author={self.author}," \
               f" addresses={self.addressees}, name={self.name})"


Base.metadata.create_all(engine)
