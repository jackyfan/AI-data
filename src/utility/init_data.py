from dal.database import SQLiteDB
import uuid
from utility.logger_helper import LoggerHelper

logger = LoggerHelper.get_logger(__name__)

def init_data(db_name="example.sqlite3"):
    db = SQLiteDB(db_name)
    db.connect()
    db.execute("""
    CREATE TABLE IF NOT EXISTS user_login (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vopenid TEXT NOT NULL, 
        dtstatdate datetime NOT NULL
    )
    """, None)
    db.execute("""
    CREATE TABLE IF NOT EXISTS user_pay (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vopenid TEXT NOT NULL,
        dtstatdate datetime NOT NULL,
        imoney int NOT NULL
    )
    """, None)
    vopenid1 = uuid.uuid4().hex
    vopenid2 = uuid.uuid4().hex

    db.execute("INSERT INTO user_login (vopenid,dtstatdate) VALUES (?,?)", (vopenid1, "2025-06-09 12:12:00"))
    db.execute("INSERT INTO user_login (vopenid,dtstatdate) VALUES (?,?)", (vopenid1, "2025-06-10 12:13:00"))
    db.execute("INSERT INTO user_login (vopenid,dtstatdate) VALUES (?,?)", (vopenid1, "2025-06-11 12:14:00"))

    db.execute("INSERT INTO user_login (vopenid,dtstatdate) VALUES (?,?)", (vopenid2, "2025-06-10 12:12:00"))
    db.execute("INSERT INTO user_login (vopenid,dtstatdate) VALUES (?,?)", (vopenid2, "2025-06-11 12:13:00"))
    db.execute("INSERT INTO user_login (vopenid,dtstatdate) VALUES (?,?)", (vopenid2, "2025-06-12 12:14:00"))

    db.execute("INSERT INTO user_pay (vopenid,dtstatdate,imoney) VALUES (?,?,?)", (vopenid1, "2025-06-01 12:12:00", 90))
    db.execute("INSERT INTO user_pay (vopenid,dtstatdate,imoney) VALUES (?,?,?)", (vopenid1, "2025-06-02 12:12:00", 80))
    db.execute("INSERT INTO user_pay (vopenid,dtstatdate,imoney) VALUES (?,?,?)", (vopenid1, "2025-06-03 12:12:00", 100))

    db.execute("INSERT INTO user_pay (vopenid,dtstatdate,imoney) VALUES (?,?,?)", (vopenid2, "2025-06-01 12:12:00", 40))
    db.execute("INSERT INTO user_pay (vopenid,dtstatdate,imoney) VALUES (?,?,?)", (vopenid2, "2025-06-02 12:12:00", 50))
    db.execute("INSERT INTO user_pay (vopenid,dtstatdate,imoney) VALUES (?,?,?)", (vopenid2, "2025-06-03 12:12:00", 60))

    logger.debug(db.query("SELECT * FROM user_login"))
    logger.debug(db.query("SELECT * FROM user_pay"))

    db.close()

if  __name__ == "__main__":
    init_data()