"""
错误码说明
第1~2位: 01 ~ 99, 表示产品,
第3~5位: 001 ~ 999, 表示功能/模块
第6~8位: 001 ~ 999, 表示具体错误
"""

error_code_list = {
    # 无错误
    'ok': '000000|',

    # 系统错误 001
    'error': '001001|',  # 自定义错误
    'system_error': '001002|系统错误',
    'not_found': '001003|404未找到',
    'permission_denied': '001004|权限不足',
    'param_error': '001005|参数错误',


    # 数据库 002
    'row_not_found': '002001|记录未找到',
    'create_row_fail': '002002|创建记录失败',
    'update_row_fail': '002003|更新记录失败',
    'delete_row_fail': '002004|删除记录失败',
    'row_exists': '002005|记录已存在',

    # 用户 003
    'token_missing': '003001|缺少Token',
    'invalid_token': '003002|错误Token',
    'invalid_auth_params': '003003|用户名或密码错误',
    'invalid_old_password': '003004|用户密码错误',
    'invalid_new_password': '003005|用户新密码错误',

}
