from utility.config import Config

def test_config():
     config = Config()
     level = config.get("logging","level")
     print(f'{level}')

if  __name__ == "__main__":
    test_config()
