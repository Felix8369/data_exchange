import uuid, time
from flask import g, request, current_app
from werkzeug.datastructures import FileStorage
from app.models.user import UserModel
from app.resources import BaseResource, ApiResource
from app.services.response import res_json
from app.repositories.user import UserRepository
from app.utils.hash import gen_md5
from app.utils.helpers import get_client_ip, not_empty_string, genrate_jwt_token
from app.utils.files import remove_file_by_link, save_uploaded_image
from app.services.decorators import api_auth


class AuthLoginResource(BaseResource):
    """
    用户登录
    """

    def post(self):
        self.parser.add_argument('username', type=not_empty_string, location="json", required=True)
        self.parser.add_argument('password', type=not_empty_string, location="json", required=True)
        args = self.parse_args()

        username = args.get('username')
        password = gen_md5(args.get('password'))
        user = UserModel.get_model_by_fields(username=username, password=password, deleted_at=0)
        if user is None:
            return res_json(code='invalid_auth_params')

        try:
            # 填写当前登录信息
            user.login_ip = get_client_ip(request)
            user.login_time = int(time.time())

            user_data = user.res_format(password=False, token_expires=False, deleted_at=False)

            # 更新 Api token
            new_token = gen_md5(str(uuid.uuid4()))
            UserRepository.update_user_token_by_model(user, new_token)

            user_data['api_token'] = genrate_jwt_token(new_token, current_app.config.get("SECRET_KEY"),
                                                       current_app.config.get("USER_VALIDITY"))
        except Exception as e:
            current_app.logger.error(e)
            return res_json(code='user_login_fail')

        return res_json(data=user_data)


class AuthLogoutResource(ApiResource):
    """
    用户登出
    """

    def post(self):
        try:
            UserRepository.update_user_token_by_model(g.user, '')
        except Exception as e:
            current_app.logger.error(e)
            return res_json(code='user_logout_fail')

        return res_json()


class AuthProfileResource(ApiResource):
    """
    用户基本信息
    """

    def get(self):
        """获取认证用户信息"""
        return res_json(data=UserRepository.gen_profile_user_data(g.user))

    def patch(self):
        """更新认证用户信息"""
        self.parser.add_argument('display_name', type=not_empty_string, location='form', required=True)
        self.parser.add_argument('old_password', type=str, location='form', trim=True, default='')
        self.parser.add_argument('new_password', type=str, location='form', trim=True, default='')
        self.parser.add_argument('new_password2', type=str, location='form', trim=True, default='')
        self.parser.add_argument('image', type=FileStorage, location='files')
        args = self.parse_args()

        # 检查姓名格式
        if not UserRepository.check_display_name(args.get('display_name')):
            return res_json(code='invalid_display_name')

        # 检查是否修改密码
        if args.get('old_password') != '':
            if gen_md5(args.get('old_password')) != g.user.password:
                return res_json(code='invalid_old_password')
            if args.get('new_password') == '' or args.get('new_password2') == '' or args.get('new_password') != args.get('new_password2'):
                return res_json(code='invalid_new_password')

            # 检查密码格式
            if args.get('new_password') == g.user.username:
                return res_json(code='same_username_password')
            if not UserRepository.check_password(args.get('new_password')):
                return res_json(code='invalid_password')

            args['api_token'] = ''  # 已经修改了密码, 需要重新登录
            args['new_password'] = gen_md5(args.get('new_password'))
        else:
            args['api_token'] = g.user.api_token
            args['new_password'] = g.user.password

        # 检查头像后缀
        # if args.get('image') is not None:
        #     if not check_image_extension(args.get('image')):
        #         return res_json(code='invalid_image_extension')

        old_image = g.user.image
        try:
            # 头像
            args['image'] = save_uploaded_image(current_app, args.get('image'), 'profile_')

            UserRepository.update_user_profile_by_model(g.user, args.get('display_name'), args.get('new_password'),
                                                        args.get('api_token'), args.get('image'))
        except Exception as e:
            current_app.logger.error(e)
            remove_file_by_link(current_app, args['image'])
            return res_json(code='update_profile_fail')

        # 清除旧头像文件
        if args.get('image') is not None:
            remove_file_by_link(current_app, old_image)

        # # 添加日志
        # UserLogRepository.create_user_log(g.user.id, g.user.id, UserLogModel.TYPE_USER, UserLogModel.ACTION_UPDATE,
        #                                   get_client_ip(request))

        # 返回更新后的用户信息
        user = UserRepository.get_user_by_id(g.user.id)

        return res_json(data=UserRepository.gen_profile_user_data(user))


