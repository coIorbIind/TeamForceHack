from typing import Optional


class BotConfig:
    """
    Class for keeping config data
    """
    bot_token = None
    # можно добавить валидацию по размеру


def load_config(path: str, delimiter: str = ':') -> Optional[BotConfig]:
    """
    Function for loading config file
    :param path: path to config file
    :param delimiter: delimiter for data in config file
    :return: instance of BotConfig class or None if there were errors while reading the file
    """
    result = BotConfig()

    try:
        with open(path) as file:
            for line in file:
                split_line = [item.strip() for item in line.split(delimiter)]
                if len(split_line) != 2:
                    raise ValueError

                else:
                    key = split_line[0]
                    value = split_line[1]

                if hasattr(result, key):
                    result.__setattr__(key, value)
        return result
    except OSError:
        return None
    except ValueError:
        return None
