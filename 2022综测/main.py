import time
import requests
import base64
import json

api = {
    'check': 'https://we.cqupt.edu.cn/api/lxsp/get_lxsp_list_gxw20210316.php',
    'apply': 'https://we.cqupt.edu.cn/api/lxsp/post_lxsp_spxx_test0914.php',
    'cheat': 'https://we.cqupt.edu.cn/api/lxsp/post_lxsp_sm_test20210311.php'
}


def json_query(sub_api, data: dict):
    data['timestamp'] = round(time.time())
    res = requests.post(api[sub_api], {
        'key': base64.b64encode(json.dumps(data).encode()).decode()
    })
    try:
        return json.loads(res.text)
    except Exception as e:
        print(e)
        return {}


def check_status(number, openId) -> (bool, str, str):
    """
    返回申请状态，若暂无申请，则为 False
    :param number: 学号
    :param openId: openId
    :return: 目前是否有申请
    """
    data = {"openid": openId, "xh": number, "page": 1}
    res = json_query('check', data)
    # print(res)
    if 'data' in res and res['data'] is not None:
        if res['data']['result'] is None:
            return False, '无记录 或 openid 错误', ''
        if res['data']['result'][0]['lczt'] == '结束':
            return False, '无记录', ''
    return True, res['data']['result'][0]['lczt'], res['data']['result'][0]['log_id']


def apply_for(number, openId, name, college, grade):
    data = {"xh": number, "name": name, "xy": college, "nj": grade,
            "openid": openId, "wcmdd": "重庆市,重庆市,南岸区",
            "qjsy": "干饭", "wcxxdd": "校外",
            "sfly": "请选择",
            "wcrq": time.strftime('%Y-%m-%d'),
            "qjlx": "市内当日离返校",
            "yjfxsj": time.strftime('%Y-%m-%d'),
            "beizhu": ""}
    res = json_query('apply', data)
    return res


def cheat(out_type, number, openid, log_id):
    res = json_query('cheat', {
        'openid': openid,
        'xh': number,
        'type': out_type,
        'log_id': log_id,
        'location': '崇文门',
        'latitude': 29.53589022162327,
        'longitude': 106.60067455853019
    })
    if 'data' in res:
        if res['data']['type'] == out_type:
            return True
    return False


def cqupt_cheat(temp, c_type):
    _, flag, log_id = check_status(temp['number'], temp['openid'])
    if flag == '待出校' and c_type == '离':
        res = cheat('出校', temp['number'], temp['openid'], log_id)
        if res:
            return '出校成功！'
    if flag == '待入校' and c_type == '返':
        res = cheat('入校', temp['number'], temp['openid'], log_id)
        if res:
            return '入校成功！'
    return '存在记录与类型不匹配！'


# 申请出校
def cqupt_gout(temp):
    """
    temp = {
        "number": 学号,
        "openid": openid,
        "name": 姓名,
        "college": 学院,
        "grade": 年级
    }

    :param temp: 用户预制模板
    :return:
    """
    status, flag, _ = check_status(temp['number'], temp['openid'])
    if status:
        return f'存在{flag}记录！跳过申请'
    else:
        res = apply_for(temp['number'], temp['openid'], temp['name'], temp['college'], temp['grade'])
        if res['message'] == 'OK':
            return '创建成功！'


ybw = {
    "number": 2019210363,
    "openid": "oIaII0SD_k5Dfqx3vTT887hOu1ac",
    "name": "由博文",
    "college": "计算机学院",
    "grade": 2019
}
cry = {
    "number": 2019211486,
    "openid": "oIaII0QI-JZQoGGEYx-Ue6vEvnn0",
    "name": "曹润艺",
    "college": "计算机学院",
    "grade": 2019
}
# cqupt_gout(cry)
cqupt_cheat(cry, '离')

