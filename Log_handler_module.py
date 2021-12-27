import datetime
import logging
from File_handler_module import File_Handler

class Log_handler:
    """
    this clss is for registering logs
    :params logger , f_handler
    metods: log to add log
    """

    log_file = 'log_file.log'
    def __init__(self):
        self.logger = None
        self.f_handler = None


    @staticmethod
    def log(time,message,event_type):
        logger = logging.getLogger(__name__)
        f_handler = logging.FileHandler('log_file.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(formatter)
        logger.addHandler(f_handler)
        logger.level = logging.NOTSET
        logger.setLevel(logging.INFO)
        if event_type == 'INFO':
            logger.info(message)
        elif event_type =="ERROR" or event_type == 'EXCEPTION':
            logger.error(message)


