from dal.database import SQLiteDB
from utility.logger_helper import LoggerHelper

logger  = LoggerHelper.get_logger(__name__)
def test_database():
    db = SQLiteDB("test.sqlite3")
    db.connect()
    db.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)", None)
    db.execute("INSERT INTO test (name) VALUES (?)", ("test",))
    logger.debug(db.query("SELECT * FROM test"))
    db.close()

if  __name__ == "__main__":
    test_database()