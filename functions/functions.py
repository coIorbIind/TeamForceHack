


def get_topics(username: str) -> list:
    """
    Function for getting topics of the author
    :param username: author's username
    :return: list of author's topics or None
    """
    # get from DB
    topics = list()
    return topics


def get_addressees(topic: str) -> list:
    """
    Function for getting addressees of the topic
    :param topic: topic title for getting addressees
    :return: list of addressees
    """
    # get from DB
    addressees = None
    if addressees is None:
        addressees = list()
    return addressees


def create_topic(username: str, topic_name: str, addressees: list) -> bool:
    """
    Function for creating new topic
    :param username: author's username
    :param topic_name: name of new topic
    :param addressees: addressees for mailing
    :return: True - if topic was created, else - if it wasn't
    """
    # get ot create author user

    for address in addressees:
        pass
        #  get ot create address user

    # create topic
