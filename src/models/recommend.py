import requests


def recommend_data_assets(user_input, topK):
    """
    根据自有模型推荐数据资产
    :param user_input: 用户输入，用于模型的推荐
    :param topK: 推荐的前K个数据资产
    :return: 推荐的前K个数据资产列表
    """
    # 设置头部
    heads = {'Content-Type': 'application/json'}
    # 构造参数数据
    data = {
        'text': user_input,
        'topK': topK
    }
    # 调用API
    # url = 'https://192.168.1.2/recommend_data_assets'
    # response = requests.post(url, json=data, headers=headers)
    # answer = response.json()

    answer = {'code': 0, 'data': ['user_login', 'user_levelup', 'user_pay']}
    return answer


def recommend_data_asset(table):
    return "user_login"