import datetime


def requirement_clarification(user_query, domain_info):
    """
    需求澄清提示词
    :param user_query:用户问题
    :param domain_info:业务知识
    :return:
    """
    template = """
       你是游戏领域资深的数据分析专家，擅长仔细思考并回答问题。
       ##目标
       接收用户提供的需求查询和业务知识，判断是否有不清楚的取数逻辑并向用户提问。

       ##限制
       1.按顺序列出问题，每个问题以请字开头；
       2.库表信息在后续补充，当前先忽略库表信息；
       3.只询问影响取数SQL代码的模糊信息部分，不需要询问常识问题；
       4.如果用户没有提到的维度，不需要问维度；
       5.如果问题已清晰，请输出问题已澄清。

       ##参考示例
       用户问题：昨天活跃的用户，钻石段位有多少。提问：请问钻石段位的取数逻辑是什么？
       用户问题：统计上周，活跃玩家中有英雄会的玩家数？业务知识：有英雄会的玩家意思为工会ID不为0。提问：请问有英雄会的玩家取数逻辑是否为"工会ID不为0"？
       用户问题：统计近7天购买红宝石的人数。提问：请问购买红宝石的取数逻辑是什么？
       用户问题：统计上个月活跃的玩家数。提问：问题已澄清。

       ## 输入
       【用户问题】
       {user_query}

       【业务知识】
       {domain_info}
    """
    return template.format(user_query=user_query, domain_info=domain_info)


def knowledge_extraction(chats):
    """
    知识抽取提示词
    :param chats:
    :return:
    """
    template = """
    你是游戏领域资深的数据分析专家，擅长仔细思考并回答问题。
    ##目标
    从聊天记录中抽取业务知识，并按统一的模板进行组织。
    ##限制
    1.业务知识关注游戏内部机制、规则或者对玩家行为的定义和解释；
    2.排除数据分析任务参数，如数据集大小、输出字段等相关信息；
    3.输出中的title为知识的统称；
    4.输出中的type可以从[活跃,付费,玩法,社交]中选取，多个输出请用｜拼接；
    5.输出中的facts记录每个知识点的具体信息。
    ##参考示例
    【输入】
    usera:统计上周参与游戏A中的玩法1和玩法2的人数。
    userb：玩法1和玩法2的取数逻辑是什么？
    usera：玩法表中，mode=1和mode=2
    【输出】
    {
        "title": "子模式",
        "type": "玩法",
        "query_list": [
            "统计上周参与游戏A中的玩法1和玩法2的人数"
        ],
        "facts": [
            {
                "name": "玩法1",
                "value": "玩法表中，mode=1"
            },
            {
                "name": "玩法2",
                "value": "玩法表中，mode=2"
            },
        ],

        "emb_keys": [
            "$.title",
            "$.facts[*].name"
        ]
    }
    ##输入
    {chats}
    """
    return template.format(chats=chats)


def requirement_rewriting(user_query, domain_info):
    """
    需求改写提示词
    :param user_query:用户问题
    :param domain_info:业务知识
    :return:
    """
    template = """
        你是游戏领域资深的数据分析专家，擅长仔细思考并回答问题。
        
        ##目标
        接收用户提供的需求查询和业务知识，对用户的查询进行改写。
        
        ##限制
        改写后的需求语义不发生改变，使得问题描述更清晰、没有歧义即可；
        今天是{now_date}，规范查询中的日期格式。如果没提及具体时间，默认添加最近7天；如果缺少年份或月份，则根据今天的日期补充年份和月份，确保日期格式为××××年××月××日；
        根据提供的业务知识扩写查询中的术语；
        每条业务知识有一个相关度（得分为0～1），根据相关度得分考虑是否使用该知识；
        如果问题已清晰，请输出原问题，不需要改写。
        
        ##参考示例
        【用户问题】
        统计上周活跃玩家中有英雄会的数量？
        
        【业务知识】
        有英雄会的玩家意思为工会ID不为0。
        
        【输出】
        统计上周活跃玩家中有英雄会（工会ID不为0）的数量
        
        ##输入
        【用户问题】
        {user_query}
        
        【业务知识】
        {domain_info}
    """
    return template.format(user_query=user_query, domain_info=domain_info, now_date=datetime.datetime.now().strftime("%Y年%m月%d日"))


def requirement_synthesis(table_info, examples):
    """
    需求合成
    :param table_info: 资产表信息
    :param examples: 参考示例
    :return:
    """
    template = """
    你是游戏领域资深的数据分析师，给定资产表信息和参考示例，仿照示例，生成10个需求描述。
    ## 资产表信息
    {table_info}
    ## 参考示例
    {examples}
    每行输出一个需求描述，无须其他解释信息。
    """
    return template.format(table_info=table_info, examples=examples)


def precise_ranking_fine_tuning(table_info, examples, question):
    """
    精排微调
    :param table_info: 资产表信息
    :param examples: 参考示例
    :param question: 用户需求
    :return:
    """
    template = """
        你是游戏领域资深的数据分析师，给定候选资产表信息和用户需求，请从候选资产表中选择尽可能少的表来解决用户需求。
        ## 参考示例
        {examples}
        
        ## 资产表信息
        {table_info}
        
        ## 用户需求
        {question}
    """
    return template.format(table_info=table_info, examples=examples, question=question)
