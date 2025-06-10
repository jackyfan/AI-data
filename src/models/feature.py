feature_definitions = {
    "活跃用户": {
        "sql": "select dtstatdate,vopenid from user_login where dtstatdate>='{:start_date}' and dtstatdate <='{:end_date}' group by vopenid,dtstatdate",
        "description": "统计当日有过登录行为的vopenid，持续的数据能够反映游戏的受欢迎程度，也是评价游戏品质的重要指标。"
    },
    "付费用户": {
        "sql": "select dtstatdate,vopenid from user_pay where dtstatdate>='{:start_date}' and dtstatdate <='{:end_date} grouped by dtstatdate,vopenid,'",
        "description": "每天付费用户"
    },
    "付费总额": {
        "sql": "select dtstatdate,vopenid,sum(imoney) from user_pay where dtstatdate>='{:start_date}' and dtstatdate<='{:end_date}'",
        "description": "当天用户付费的总额"
    }
    # more features
}


def get_feature_definition(feature_name):
    """
    获取指标特征定义
    :param feature_name: 指标特征的名称
    :return: 指标特征的定义，包括类型和描述。如果不存在，返回None
    """
    result = {}
    for ft, val in feature_definitions.items():
        if feature_name in ft or ft in feature_name:
            result[ft] = val
    return result
