import logging
import os
import sys
from utility.config import Config
from logging import handlers


class LoggerHelper:
    @staticmethod
    def get_logger(name):
        """
        获取日志记录器
        :param name:
        :return: 日志对象
        """
        config = Config()
        logger = logging.getLogger(name)

        if not logger.hasHandlers():
            log_file = config["logging"].get('file', 'application.log.default')
            # 创建日志目录
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            log_dir = os.path.join(project_root, 'logs', f'{log_file}')
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            log_level = config['logging'].get('level', 'DEBUG')
            # 设置按天归档文件
            th = handlers.TimedRotatingFileHandler(filename=log_file,
                                                   when=config['logging'].get('when', 'D'),
                                                   backupCount=config['logging'].get('backCount', 7),
                                                   encoding='utf-8')
            th.setLevel(log_level)
            formatter = logging.Formatter(config['logging'].get('fmt', '%(asctime)s-%(levelname)s-%(message)s'))
            # 设置日志格式
            th.setFormatter(formatter)
            # 明确指定日志输出到标准输出流中
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)

            logger.addHandler(th)
            logger.addHandler(console_handler)
            logger.setLevel(log_level)
        return logger
