import configparser
import os


class Config:
    """
    单例模式
    """
    _instance = None

    def __new__(cls, *arg, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *arg, **kwargs)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        self.config = configparser.ConfigParser()
        # 读取环境变量，如果未设置，返回development
        environment = os.getenv('APP_ENV', 'development')
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        path = os.path.join(project_root, 'config', f'config_{environment}.ini')
        if not os.path.exists(path):
            raise ValueError(f'Not Found Config file path：{path}')
        self.config.read(path, encoding='gbk')

    def __getitem__(self, section):
        return self.config[section]

    def get(self, section, option):
        return self.config.get(section, option)
