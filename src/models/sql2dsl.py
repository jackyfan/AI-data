

def sql_to_dsl(sql):
    template = """
    你是一名资深数据开发人员,你将接收"输入SQL",按照以下"步骤"一步一步思考，严格按照"示例"的格式输出，最终生成一个符合要求的JSON。
    ##步骤：
    识别"输入SQL"并去掉"输入SQL"中的字段别名，拆分为5部分，分别为"查询字段"、"字段类型"、"来源表"、"关联关系"和"筛选条件"，字段类型包含"维度"和"指标"
    识别"筛选条件"中的字段，作为"筛选字段"
    将"来源表"按格式填入"输出JSON"的tables中
    将"关联关系"按格式填入"输出JSON"的"join_conditions"中，"join_conditions"中的op只可以是">、>=、<、<=、="中的一个。
    将"查询字段"和"筛选字段"按格式填入"输出JSON"的"select_fields"中，如果"select_fields"中有来源于不同表但"name"相同的字段，则创建字段别名"alias"，如果没有则"alias"留空，创建方法为"table_label"拼接"name"。
    将步骤4中的"alias"(如果alias为空则使用"name")根据去掉了字段别名的"输入SQL"的逻辑填入"输出JSON"的"select_fields"中"ret"中，需要注意的是"ret"中的"columnName"都是步骤4中的"alias"或"name"。其中维度字段和直接count、sum、max、min计算的指标（比如count(distinctrole_id)就是直接计算的指标，count(distinctcasewhenview_cnt>0thenrole_idelsenullend)就不是直接计算的指标）放到"dataSetCols"中，不是直接计算的指标放到"complexCols"中。"complexCols"中的参数只替换字段，不替换常数值，比如count(distinctcasewhenview_cnt>10thenrole_idelsenullend)只替换view_cnt和role_id，不替换"10"。
    将"筛选条件"中除了日期筛选的其他筛选条件按格式填入"输出JSON"的"conditionSetCols"中，"conditionSetCols"中的op为枚举值">,<,>=,<=,=,≠,is_null,not_null,in,notin，包含，不包含，为空，不为空,非空"中的一个。
    将"筛选条件"中的日期筛选放到"ret"的"dateType"中，如果是3个连续日期就是最近3天，如果是7个日期就是最近7天，dateType的枚举值"今天、昨天、本周、上周、过去7天、过去30天、过去60天、本月、上月、过去3个月、过去6个月、上半年"中的一个。
    
    根据"示例输出SQL"和"示例输出JSON"输出最终的结果
    ##示例输入SQL：
    {select
        t1.ds, --日期
        t2.mode_id, --模式ID
        T1.active_user_cnt_day, --活跃用户数
        from
        表 T1 left join 表 T2
        on t1.user_id = t2.user_id
        where
        t1.ds = systemdate
    }
    
    ## 示例输出JSON：
    {
        "join_info":
        {
    
            "join_tables": [
            {
                "dataset_id": "",
                "label": "t1",
                "name": "用户分模式日增量表",
                "tb_name": "表1"
            },
            {
                "dataset_id": "",
                "label": "t2",
                "name": "用户登录表",
                "tb_name": "表2"
            }],
            ...
            "ret":
            {
                "dateType": "当日7天",
                "figureType": "表格",
                "dataSetCols": [
                    {
                        "columnName": "t1role_id",
                        "columnType": "指标",
                        "computeType": "去重数",
                        "comment": "活跃用户数"
                    }
                }]
        }
    }
    ## 输入SQL
    {slq}
    """