"""Basic logging setup for the application."""
import logging

logger = logging.getLogger('BotLogger')
logger.setLevel(logging.DEBUG)

# create a file handler for BotLogger
handler = logging.FileHandler('app.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
