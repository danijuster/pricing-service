import logging


# create logger
logger = logging.getLogger('pricing_service')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.FileHandler('log//logs.txt')
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
