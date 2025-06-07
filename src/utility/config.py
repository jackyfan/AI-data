import configparser
import os


class Config:
    _instance = None

    def __new__(cls, *arg, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *arg, **kwargs)
            cls._instance.__init__()

    def __init__(self):
        self.config = configparser.ConfigParser()
        #读取环境变量，如果未设置，返回development
        environment = os.getenv('APP_ENV', 'development')
        self.config.read(f'config/config_{environment}.ini')

    def get(self, section, option):
        return self.config.get(section, option)
