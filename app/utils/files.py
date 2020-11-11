import os
import uuid
import datetime

ALLOW_IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'bmp')


def remove_file(path):
    """
    删除文件
    :param path: 文件绝对路径
    :return:
    """

    if path is not None and str(path).strip() != '':
        try:
            os.remove(path)
        except:
            pass


def check_avatar_size(file, max_size) -> bool:
    """
    检查头像文件大小
    :param file: FileStorage
    :return:
    """

    if file is None:
        return True

    file_len = get_sizes_by_list(file)
    if file_len > max_size:
        return False

    return True


def get_sizes_by_list(file):
    """
    根据文件列表获取总大小
    :param file: FileStorage
    :return:
    """
    sizes = 0
    file.seek(0, os.SEEK_END)
    sizes += file.tell()
    file.seek(0)  # 指针归零

    return sizes


def remove_file_by_link(app, link, link_prefix='uploads'):
    """
    根据访问地址删除文件
    :param app: Flask app
    :param link: 页面访问地址
    :param link_prefix: 访问地址前缀
    :return:
    """

    upload_dir = app.config.get('UPLOAD_DIR')
    if upload_dir is None or upload_dir.strip() == '':
        return

    rel_path = link.replace('/{}/'.format(link_prefix.strip('/')), '', 1).strip('/')
    abs_path = os.path.join(upload_dir, rel_path)
    remove_file(abs_path)


def check_file_extension(file, allow_suffix=ALLOW_IMAGE_EXTENSIONS) -> bool:
    """
    检查图片后缀
    :param file: FileStorage 对象 (from werkzeug.datastructures import FileStorage)
    :return:
    """

    if file is None:
        return True
    if len(allow_suffix) == 0:
        return True

    # 后缀名不存在
    if len(file.filename.split('.')) < 2:
        return False

    ext = file.filename.split('.')[-1].lower()
    if ext in allow_suffix:
        return True

    return False


def save_uploaded_image(app, file, name_prefix='', public_link=True, link_prefix='uploads'):
    """
    保存上传文件图片
    :param app: Flask app
    :param file: FileStorage 对象 (from werkzeug.datastructures import FileStorage)
    :param name_prefix: 文件名称前缀
    :param public_link: 是否返回访问地址
    :param link_prefix: 访问地址前缀
    :return: None or abspath or public link
    """

    # 检查是否有文件
    if file is None:
        return None

    upload_dir = app.config.get('UPLOAD_DIR')
    if upload_dir is None or upload_dir.strip() == '':
        raise Exception('App config [UPLOAD_DIR] missing')

    # 检查文件后缀名
    if not check_file_extension(file):
        raise Exception('Invalid image extension')

    # 按照日期创建目录
    current_date = datetime.today().strftime('%Y%m%d')

    file_ext = file.filename.split('.')[-1].lower()
    name_prefix = name_prefix or ''
    new_filename = '{}{}_{}.{}'.format(name_prefix, str(uuid.uuid4()), str(int(time.time())), file_ext)
    filepath = os.path.join(upload_dir, current_date, new_filename)

    # 检查目录是否存在
    if not os.path.isdir(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except Exception as e:
            raise e

    # 保存文件
    try:
        file.save(filepath)
    except Exception as e:
        raise e

    if public_link:
        return '/{}/{}/{}'.format(link_prefix.strip().strip('/'), current_date, new_filename)

    return filepath
