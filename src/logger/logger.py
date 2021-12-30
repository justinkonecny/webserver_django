# Configure the logging string
import logging
from typing import Union

logging.basicConfig(
    format='[%(levelname)s][%(asctime)s][%(name)s] %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S %p'
)


# The default logging level to apply to the logger
def get_logger(name: str, level: Union[str, int] = logging.ERROR) -> logging.Logger:
    """
    Instantiates a logger with the given name and sets the level to the
    level param.
    :param name: The module name this logger is being created for
    :param level: The log level to print to the console
    :return: The newly created logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
