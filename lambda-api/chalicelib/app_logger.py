'''Setup logger for the application'''
import logging


logger = logging.getLogger()
logger.setLevel(logging.WARNING)


def log(error):
    '''Logs an error to stdout'''
    logger.error('{}: {}'.format(type(error).__name__, error))
    logger.exception(error)
