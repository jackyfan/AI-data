from datetime import datetime
#修正SQL
def correct_sql(sql,db_error,history,db,model_name):
    currdate = datetime.now().strftime("%-Y%m-%d")

    system_prompt=f"""
        作为一名专业游戏数据分析师，你非常熟悉游戏行业并且擅长SQL代码开发。你将根据用户提供的SQL代码及数据库返回的错误信息，为用户写出正确的SQL代码。
        -当前日期是{currdate}
        -特别注意，数据库的错误信息和用户信息中的内容可以提升编写SQL代码的成功率。
        -你仅能生成select查询语句。
    """

    user_prompt = f"""
        ##数据库错误信息
        {db_error}
        
        ##sql_input:
        {sql}
        特别注意，即将与程序对接，确保SQL代码简洁、准确。
        严格按照如下JSON格式输出：
        {{"reflect":(对SQL错误较为详细的反思)...,"sql":"..."}}
    """
    messages = [SystemMessage()]