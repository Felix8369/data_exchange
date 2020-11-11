import hashlib


def gen_md5(s: str) -> str:
    """
    生成 MD5 字符串
    :param s:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.hexdigest().upper()


def file_md5(file_path: str) -> str:
    """
    根据文件内容生成 MD5
    :param file_path:
    :return:
    """

    md5_str = ''
    try:
        with open(file_path, 'rb') as file:
            data = file.read()

        md5 = hashlib.md5(data)
        md5_str = md5.hexdigest()
    except:
        pass

    return md5_str
