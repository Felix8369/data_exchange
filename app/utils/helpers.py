import hashlib, binascii, os, ipaddress, time, random, string, re
from itsdangerous import TimedJSONWebSignatureSerializer as Its

def hash_password(password: str) -> str:
    """
    生成密码哈希
    :param password:
    :return:
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwd_hash = binascii.hexlify(pwd_hash)
    return (salt + pwd_hash).decode('ascii')


def verify_password(stored_password: str, provided_password: str) -> bool:
    """
    验证密码
    :param stored_password:
    :param provided_password:
    :return:
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwd_hash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwd_hash = binascii.hexlify(pwd_hash).decode('ascii')
    return pwd_hash == stored_password


def page_to_offset(page: int, page_size: int) -> tuple:
    """
    根据页码信息生成query limit数据
    :param page:
    :param page_size:
    :return:
    """

    if page < 0:
        page = 1
    if page_size < 0:
        page_size = 10
    if page_size > 100:
        page_size = 100

    offset = (page - 1) * page_size

    return offset, page_size


def get_client_ip(request):
    """
    获取客户端 IP 地址
    :param request:
    :return:
    """

    proxy_ip = request.headers.get('X-Forwarded-For')
    if proxy_ip is not None:
        return proxy_ip.split(',')[0]
    else:
        return request.remote_addr


def to_integer(v):
    """
    转整形
    :param v:
    :return:
    """

    try:
        v = int(v)
        return v
    except:
        return 0


def verify_ids(ids: str or list):
    """
    验证删除 url 后缀 eg: api/1,2,3
    不能为  0 空 重复
    """
    if not isinstance(ids, (str, list)):
        return False
    if isinstance(ids, str):
        ids = ids.split(',')

    ids_list = []
    for i in ids:
        i = to_integer(i)
        if i == 0:
            return False
        ids_list.append(i)

    if len(ids_list) == 0:
        return False
    if len(ids_list) != len(set(ids)):
        return False
    return ids_list


def not_empty_string(s):
    """
    检查字段是否为空
    :param s:
    :return:
    """

    if not isinstance(s, str):
        raise TypeError("Must be type 'str'")

    s = s.strip()
    if not s:
        raise ValueError("Must not be empty string")

    return s



def check_time_str_not_empty(s):
    """
    检查时间字符串是否为空
    :param s:
    :return:
    """

    if not isinstance(s, str):
        raise TypeError("Must be type 'str'")

    s = s.strip()
    try:
        time_arr = time.strptime(s, "%Y-%m-%d %H:%M:%S")
        time.mktime(time_arr)

        return s
    except:
        raise ValueError("Invalid time string '{}'".format(str(s)))


def check_time_str_to_int(s):
    """
    检查时间字符串并返回时间戳
    :param s:
    :return:
    """

    if s is None:
        return None

    if not isinstance(s, str):
        raise TypeError("Must be type 'str'")

    s = s.strip()

    if s == '':
        return None

    try:
        time_arr = time.strptime(s, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(time_arr)

        return timestamp
    except:
        raise ValueError("Invalid time string '{}'".format(str(s)))


def comma_to_tuple(s):
    """
    将以逗号分割的字符串转元组
    :param s:
    :return:
    """

    if s is None:
        return None

    if not isinstance(s, str):
        raise TypeError("Must be type 'str'")

    s = s.strip()
    if s == '':
        return tuple()
    else:
        return tuple(s.split(','))



def check_input_str(s: str, min_len=None, max_len=None, chinese=False, letters=False, numbers=False, chars=None,
                    strict=False):
    """
    检查用户输入字符串
    :param s:
    :param min_len: 最小长度
    :param max_len: 最大长度
    :param chinese: 支持中文
    :param letters: 支持字母
    :param numbers: 支持数字
    :param chars: 支持自定义字符
    :param strict: 是否严格检查
    :return:
    """

    # 是否检查类型
    if not isinstance(s, str):
        return not strict

    s_len = len(s)
    if isinstance(min_len, int) and s_len < min_len:
        return False
    if isinstance(max_len, int) and s_len > max_len:
        return False

    allow_chars = ''
    if isinstance(chars, str):
        new_chars = ''
        for c in chars:
            if c == ' ':
                new_chars += '\\s'
            elif c == '\\':
                # 目前没有针对匹配'\'的字符, 直接跳过
                continue
            else:
                new_chars += '\\' + c
        allow_chars += new_chars
    if numbers:
        allow_chars += '0123456789'
    if letters:
        allow_chars += 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if chinese:
        allow_chars += '\\u4e00-\\u9fa5'

    if allow_chars == '':
        return True

    res = re.search('[^{}]'.format(allow_chars), s)
    if res is None:
        return True

    return False




def genrate_jwt_token(data, secret_key, expires=60):
    """生成token"""
    its = Its(secret_key, expires)
    token = its.dumps(data)
    return token.decode()


def verifty_jwt_token(token, secret_key, expires=60):
    """校验token"""
    its = Its(secret_key, expires)
    try:
        data = its.loads(token)
    except:
        return None
    else:
        return data