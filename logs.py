import logging 
from logging.handlers import TimedRotatingFileHandler


def log_setup(logname, file):
    """
    This method is utilized to add logs
    """
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    handler = TimedRotatingFileHandler(file, "midnight", interval= 1, encoding = "utf-8")
    formatter = logging.Formatter("%(asctime)s - %(ascname)s - %(asclevelname)s - %(ascmessage)s")
    handler.setFormatter(formatter)
    handler.suffix = "%y%m%d"
    logger.addHandler(handler)

    return logger