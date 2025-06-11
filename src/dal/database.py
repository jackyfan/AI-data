import sqlite3,os
from typing import List, Tuple, Any, Optional


class SQLiteDB:
    def __init__(self, db_name: str):
        """初始化SQLiteDB类，连接到指定的数据库文件。
            :param db_name: 数据库文件的名称
        """
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_dir = os.path.join(project_root, 'data', f'{db_name}')
        self.db_name = db_dir
        self.connection = None

    def connect(self):
        """链接到SQLite"""
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        """关闭SQLite"""
        if self.connection:
            self.connection.close()

    def table_info(self, table_name: str):
        sql = f"select sql from sqlite_master where type='table' and name='{table_name}'"
        result = self.query(sql)
        if len(result) > 0:
            return result[0]
        else:
            return None

    def execute(self, sql: str, params: Optional[tuple[Any, ...]]) -> None:
        """执行一个SQL命令（如INSERT、UPDATE、DELETE）
        :param sql:要执行的SQL命令
        :param params:SQL命令中使用的参数
        """
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        self.connection.commit()

    def query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple[Any, ...]]:
        """执行一个SQL查询命令，返回查询结果
        :param query:要执行的SQL查询命令
        :param params:SQL查询命令中使用的参数
        :return 查询结果，包含多个元祖，每个元祖代表一行数据
        """
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result

    def explain(self, sql: str):
        """
        执行一个SQL EXPLAIN命名，返回查询计划
        :param sql:要解释的SQL查询命令
        :return 查询计划
        """
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        try:
            cursor.execute(f'EXPLAIN {sql}')
            return {"code": 0, "msg": "success"}
        except sqlite3.Error as e:
            error_msg = f'DBType:Sqlite:\n explain SQL:EXPLAIN{sql}\n sqlite3.EROOR:{e}'
            return {"code": 1, "msg": error_msg}
