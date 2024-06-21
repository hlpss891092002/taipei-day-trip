import logging
logger = logging.getLogger(__name__)
Format = ' %(asctime)s - %(message)s'
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO, format=Format)
logger.info('This message should go to the log file')
