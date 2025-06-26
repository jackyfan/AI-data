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


def asset_information_improvement(db_name, tables_desc, foreign_keys):
    """
    资产信息完善提示词
    :param db_name: 数据库
    :param tables_desc: 表描述
    :param foreign_keys: 外键信息
    :return:
    """
    template = """
      你是游戏领域资深的数据分析专家，擅长仔细思考并回答问题。
        ## 目标
        接收数据资产表，为资产表生成表描述。
        ## 限制
        1.根据数据库的名字，识别资产所处的领域，这将为你提供资产的上下文信息；
        2.了解所有的资产表的信息以及表之间的外键关系，以便你理解资产表关系；
        3.为每张资产表生成一个简短的描述，用于解释表的用途；
        4.描述中不需要列出资产的数据列信息；
    
        5.以JSON格的式输出结果；
    
       ## 示例
    
       【数据库名字】银行系统
    
       【资产描述】
        # 表1: account
       [
        (account_id, the id of the account. examples:[11382, 11362].),
        (district_id, location of branch. examples:[77, 76, 2, 1, 39].),
        (frequency, frequency of the acount. examples:['POPLATEK MESICNE', 'POPLATEK TYDNE', 'POPLATEK PO OBRATU'].),
        (date, the creation date of the account. examples:['1997-12-29'].)
       ]
    
       # 表2: client
       [
        (client_id, the unique number. examples:[13998, 13971, 2, 1, 2839].),
        (gender, gender. Value examples:['M', 'F']. And F：female . M：male ),
        (birth_date, birth date. examples:['1987-09-27', '1986-08-13'].),
        (district_id, location of branch. examples:[77, 76, 2, 1, 39].)
       ]
    
       # 表3: loan
       [
        (loan_id, the id number identifying the loan data.examples:[4959].),
        (account_id, the id number identifying the account.examples:[10].),
        (date, the date when the loan is approved.examples:['1998-07-12'].),
        (amount, the id number identifying the loan data.examples:[1567].),
        (duration, the id number identifying the loan data.examples:[60].),
        (payments, the id number identifying the loan data.examples:[3456].),
        (status, the id number identifying the loan data.examples:['C'].)
       ]
    
       # 表4: district
        [
        (district_id, location of branch.examples:[77, 76].),
        (A2, area in square kilometers.examples:[50.5, 48.9].),
        (A4, number of inhabitants.examples:[95907, 95616].),
        (A5, number of households.examples:[35678, 34892].),
        (A6, literacy rate.examples:[95.6, 92.3, 89.7].),
       ]
       
       【外键】
       client.`district_id` = district.`district_id`
       
      【答案】
       {{
       "account": "Stores details about individual bank accounts.",
    
       "client": "Stores personal information about each client.",
    
       "loan": "Stores information about loans associated with each account.",
    
       "district": "Stores demographic and economic information about each district."
    
       }}
       ======================
       【数据库名字】{db_name}
       【资产描述】
       {tables_desc}
       【外键】
       {foreign_keys}
       【答案】
    """

    return template.format(db_name=db_name, tables_desc=tables_desc, foreign_keys=foreign_keys)

def asset_structure_matching(db_name,tables_structure,foreign_keys,question,evidence):
    template = """
        你是游戏领域资深的数据分析专家，擅长仔细思考并回答问题。
        
        ## 目标
        接收资产表结构信息、外部知识及问题，请从资产表中，选择与问题相关的数据列。
        
        ## 步骤
        1.对于每张资产表的每个数据列，检查是否与问题或外部知识相关，无关则丢弃；
        2.如果资产表的所有列都与问题或外部知识无关，则保留空数组；
        3.根据与问题、外部知识的相关性，为数据列排序；
        4.以JSON格式输出；
        
        ## 示例
        
        【数据库名字】银行系统
        
        【资产描述】
        # 表1: account,Stores details about individual bank accounts.
        [
            (account_id, the id of the account. examples:[11382, 11362].),
            (district_id, location of branch. examples:[77, 76, 2, 1, 39].),
            (frequency, frequency of the account. examples:['POPLATEK MESICNE', 'POPLATEK TYDNE', 'POPLATEK PO OBRATU'].),
            (date, the creation date of the account. examples:['1997-12-29'].)
        ]
        
        # 表2: client,Stores personal information about each client.
        [
            (client_id, the unique number. examples:[13998, 13971, 2, 1, 2839].),
            (gender, gender. Value examples:['M', 'F']. And F：female . M：male ),
            (birth_date, birth date. examples:['1987-09-27', '1986-08-13'].),
            (district_id, location of branch. examples:[77, 76, 2, 1, 39].)
        ]
        
        # 表3: loan,Stores information about loans associated with each account.
        [
            (loan_id, the id number identifying the loan data.examples:[4959].),
            (account_id, the id number identifying the account.examples:[10].),
            (date, the date when the loan is approved.examples:['1998-07-12'].),
            (amount, the id number identifying the loan data.examples:[1567].),
            (duration, the id number identifying the loan data.examples:[60].),
            (payments, the id number identifying the loan data.examples:[3456].),
            (status, the id number identifying the loan data.examples:['C'].)
        ]
        
        # 表4: district,Stores demographic and economic information about each district.
        [
            (district_id, location of branch.examples:[77, 76].),
            (A2, area in square kilometers.examples:[50.5, 48.9].),
            (A4, number of inhabitants.examples:[95907, 95616].),
            (A5, number of households.examples:[35678, 34892].),
            (A6, literacy rate.examples:[95.6, 92.3, 89.7].),
        ]
        
        【外键】
        client.`district_id` = district.`district_id`
        
        【问题】
        What is the gender of the youngest client who opened account in the lowest average salary branch?

        【外部知识】
        Later birthdate refers to younger age; A5 refers to average salary.

        【答案】
        
        ```json
        {{
        "account": [],
        "client": ["gender", "birth_date", "district_id"],
        "loan": [],
        "district": ["district_id", "A5", "A2", "A4", "A6", "A7"]
        }}
        ```
        ========================
        【数据库名字】 {db_name}
        
        【资产结构】
        {tables_structure}
        
        【外键】
        {foreign_keys}
        
        【问题】
        {question}
        
        【外部知识】
        {evidence}
        
        【答案】
    """
    return template.format(db_name=db_name, tables_structure=tables_structure, foreign_keys=foreign_keys, question=question, evidence=evidence)

