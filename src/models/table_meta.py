def get_table_asserts(db, table_name):
    """
    获取指定库表资产
    :param db: 数据库
    :param table_name: 表名称
    :return: 包含表名、表结构、表描述的词典
    """
    table_info = db.table_info(table_name)
    if table_info is None:
        return None
    return {"table_name": table_name,
            "structure": table_info[0]}
