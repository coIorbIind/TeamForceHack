from typing import Optional, List

import database.db_entities as dbe
from sqlalchemy.orm import Session


class DataBaseRunner:

    def __init__(self):
        self.engine = dbe.engine
        self.session = Session(self.engine)

    # def get_or_create(self, model, **kwargs):
    #     """
    #     Function that returns a model object
    #     according to the given parameters
    #     or creates a new one if one was not found
    #     :param model: model in DB for search
    #     :param kwargs: parameters for search
    #     :return: instance of model
    #     """
    #     instance = self.session.query(model).filter_by(**kwargs).first()
    #     if instance:
    #         return instance
    #     else:
    #         instance = model(**kwargs)
    #         self.session.add(instance)
    #         self.session.commit()
    #         return instance

    def get_topics(self, username: str) -> Optional[List[dbe.Topic]]:
        """
        Function for getting topics of the author
        :param username: author's username
        :return: list of author's topics or None
        """
        user = self.session.query(dbe.User).filter(dbe.User.tgm_link == username).first()

        if user is None:
            return None

        return user.topics

    def get_topic_by_name(self, topic_name: str) -> Optional[dbe.Topic]:
        return self.session.query(dbe.Topic).filter(dbe.Topic.name == topic_name).first()

    def get_topics_as_addressor(self, username: str) -> Optional[List[dbe.Topic]]:
        topics = self.session.query(dbe.Topic).all()
        user = self.get_user_by_username(username)
        return list(filter(lambda topic: user in topic.addressees, topics))

    # def get_addressees(self, topic_name: str) -> Optional[List[dbe.User]]:
    #     """
    #     Function for getting addressees of the topic
    #     :param topic_name: topic title for getting addressees
    #     :return: list of addressees
    #     """
    #     topic = self.session.query(dbe.Topic).filter(dbe.Topic.name == topic_name).first()
    #
    #     if topic is None:
    #         return None
    #
    #     return topic.addressees

    def get_user_by_username(self, username: str):
        return self.session.query(dbe.User).filter(dbe.User.tgm_link == username).first()

    def create_topic(self, username: str, topic_name: str, text: str, addressees: list):
        """
        Function for creating new topic
        :param username: author's username
        :param topic_name: name of new topic
        :param addressees: addressees for mailing
        :param text: welcome text
        # :return: True - if topic was created, else - if it wasn't
        """
        # get ot create author user
        author = self.get_user_by_username(username=username)
        audience = list()
        app = audience.append

        for address in addressees:
            user = self.get_user_by_username(address)
            if user is None:
                pass
            else:
                app(user)

        topic = dbe.Topic(
            name=topic_name,
            author=author,
            addressees=audience,
            text=text
        )

        self.session.add(topic)
        self.session.commit()

    def add_message(self, message: str, topic_name: str, username: str) -> bool:
        """
        Function for adding message in topic
        :param message: message for adding
        :param topic_name: title of current topic
        :param username: username of sender
        :return: was message added to topic or not
        """
        sender = self.get_user_by_username(username=username)
        topic = self.session.query(dbe.Topic).filter(dbe.Topic.name == topic_name).first()

        if topic is None:
            return False

        message_instance = dbe.Message(
            msg_text=message,
            sender=sender,
            topic=topic
        )
        self.session.add(message_instance)
        self.session.commit()

        return True

    def add_addressees(self, topic_name: str, addressees: list):
        """
        Function for adding new members to the audience
        :param topic_name: name of topic
        :param addressees: new addressees for mailing
        """
        audience = list()
        app = audience.append

        for address in addressees:
            user = self.get_user_by_username(address)
            if user is None:
                pass
            else:
                app(user)

        topic = self.session.query(dbe.Topic).filter(dbe.Topic.name == topic_name).first()

        topic.addressees += audience

        self.session.add(topic)
        self.session.commit()

    def delete_addressees(self, topic_name: str, addressees: list):
        """
        Function for deleting members from the audience
        :param topic_name: name of topic
        :param addressees: addressees for deleting
        """

        topic = self.session.query(dbe.Topic).filter(dbe.Topic.name == topic_name).first()

        audience = topic.addressees

        new_audience = list(filter(lambda item: item.tgm_link not in addressees, audience))

        topic.addressees = new_audience

        self.session.add(topic)
        self.session.commit()

    def create_user(self, username: str, chat_id: str):
        check_user = self.get_user_by_username(username=username)
        if check_user is None:
            user = dbe.User(
                tgm_link=username,
                chat_id=chat_id,
            )
            self.session.add(user)
            self.session.commit()
#
# dbr = DataBaseRunner()
# dbr.create_topic("a", "b", ["1", "2"])
