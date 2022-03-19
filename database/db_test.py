import db_entities as dbe
from sqlalchemy.orm import Session

engine = dbe.engine

session = Session(engine)

user = dbe.User(
    tgm_link="Author"
)
sender = dbe.User(
    tgm_link="Sender"
)

message = dbe.Message(
    msg_text='Hello',
    sender=sender,
)

topic = dbe.Topic(
    name='Memes',
    author=user,
    addressees=[sender],
)
# print(topic.addressees[0])
#
# session.add(user)
# session.add(sender)
# session.add(message)
# session.add(topic)

session.commit()

print(session.query(dbe.User).all())
print(session.query(dbe.Message).all())
print(session.query(dbe.Topic.all()))

