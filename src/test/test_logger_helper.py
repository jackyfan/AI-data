from utility.logger_helper import LoggerHelper

def test_logger():
    logger = LoggerHelper.get_logger("test")
    logger.debug('test')

if  __name__ == '__main__':
    test_logger()