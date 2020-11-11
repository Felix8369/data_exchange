from flask import jsonify
from app.services.error_code import error_code_list


def res_json(data=None, total=None, msg=None, code=None, ret_json=False):
    """
    返回 Api 数据
    :param data: 数据
    :param total: 总记录数
    :param msg: 错误信息
    :param code: 错误代码
    :param ret_json: 是否返回 json 结构
    :return:
    """

    data = data or []
    if total is None:
        total = len(data) if type(data) == list else 1

    if code is None:
        code = 'ok'
    elif error_code_list.get(code) is None:
        code = 'system_error'

    code, tmp_msg = error_code_list.get(code).split('|')
    msg = msg or tmp_msg

    ret = {
        'data': data,
        'total': total,
        'errMsg': msg,
        'errCode': '00{}'.format(code),
    }

    if ret_json:
        return ret
    else:
        return jsonify(ret)
