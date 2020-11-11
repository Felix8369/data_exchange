import time
from app.utils.helpers import check_input_str
from app.models import db
from app.models.user import UserModel


class UserRepository(object):
    """
    用户模型仓库
    """

    @staticmethod
    def gen_common_user_data(user: UserModel) -> dict:
        return user.res_format(password=False, token_expires=False, login_ip=False, login_time=False, deleted_at=False)

    @staticmethod
    def gen_profile_user_data(user: UserModel) -> dict:
        return user.res_format(password=False, api_token=False, token_expires=False, deleted_at=False)

    @staticmethod
    def gen_common_user_data_list(user: UserModel) -> dict:
        return user.res_format(password=False, api_token=False, token_expires=False, login_ip=False, login_time=False,
                               deleted_at=False)

    @staticmethod
    def get_user_by_id(user_id: int) -> UserModel:
        return UserModel.query.filter_by(id=user_id, deleted_at=0).first()

    @staticmethod
    def get_users_by_ids(user_ids: list) -> list:
        return UserModel.query.filter(UserModel.id.in_(user_ids), UserModel.deleted_at == 0).all()

    @staticmethod
    def get_users_by_role(role: int) -> list:
        return UserModel.query.filter_by(role=role, deleted_at=0).order_by(UserModel.id.desc()).all()

    @staticmethod
    def get_users_by_ids_and_role(user_ids: list, role: int) -> list:
        return UserModel.query.filter(UserModel.id.in_(user_ids), UserModel.role == role,
                                      UserModel.deleted_at == 0).all()

    @staticmethod
    def get_user_by_token(token: str) -> UserModel:
        return UserModel.query.filter_by(api_token=token, deleted_at=0).first()

    @staticmethod
    def get_user_by_username(username: str) -> UserModel:
        return UserModel.query.filter_by(username=username, deleted_at=0).first()

    @staticmethod
    def get_user_by_username_and_password(username: str, password: str) -> UserModel:
        return UserModel.query.filter_by(username=username, password=password, deleted_at=0).first()

    @staticmethod
    def get_user_paginate_by_role(role: int, page=1, page_size=10):
        return UserModel.query.filter_by(role=role, deleted_at=0).order_by(UserModel.id.desc()).paginate(page=page,
                                                                                                         per_page=page_size,
                                                                                                         error_out=False)

    @staticmethod
    def get_user_paginate_by_role_without_current(role: int, current_id, page=1, page_size=10):
        return UserModel.query.filter_by(role=role, deleted_at=0).filter(UserModel.id != current_id).order_by(
            UserModel.id.desc()).paginate(page=page, per_page=page_size,
                                          error_out=False)

    @staticmethod
    def get_users_count_by_role(role: int) -> int:
        return UserModel.query.filter_by(role=role, deleted_at=0).count()

    @staticmethod
    def get_train_count_by_model(user: UserModel) -> int:
        return user.user_trains.filter_by(deleted_at=0).count()

    @staticmethod
    def get_team_count_by_model(user: UserModel) -> int:
        return user.teams.filter_by(deleted_at=0).count()

    @staticmethod
    def create_user_by_dict(args):
        model = UserModel()
        model.username = args.get('username')
        model.password = args.get('password')
        model.role = args.get('role')
        model.display_name = args.get('display_name')
        model.company = args.get('company') or ''
        model.image = args.get('image') or ''
        model.created_at = int(time.time())
        model.updated_at = int(time.time())

        db.session.add(model)
        db.session.flush()
        inserted_id = model.id
        db.session.commit()

        return inserted_id

    @staticmethod
    def update_user_token_by_model(user: UserModel, new_token: str):
        user.api_token = new_token
        db.session.commit()

    @staticmethod
    def update_user_profile_by_model(user: UserModel, display_name: str, new_password: str, api_token: str, image=None,
                                     company=None):
        user.display_name = display_name
        user.password = new_password
        user.image = image or user.image
        user.company = company or user.company
        user.api_token = api_token
        user.updated_at = int(time.time())

        db.session.commit()

    @staticmethod
    def delete_user_by_models(users: list):
        try:
            for user in users:
                user.deleted_at = int(time.time())
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def check_username(s: str):
        # 3-50个字符，允许中文、字母、数字、'_'、'.'、'-'
        return check_input_str(s, min_len=3, max_len=50, chinese=True, letters=True, numbers=True, chars='_.-')

    @staticmethod
    def check_display_name(s: str):
        # 3-50个字符，允许中文、字母、数字
        return check_input_str(s, min_len=3, max_len=50, chinese=True, letters=True, numbers=True)

    @staticmethod
    def check_password(s: str):
        # 6-20个字符，允许字母、数字以及标点符号
        return check_input_str(s, min_len=6, max_len=20, letters=True, numbers=True, chars="~!@#$%^&*()-=_+[]\{\}\|\';\":/.,?><")

    @staticmethod
    def check_company(s: str):
        # 3-50个字符，允许字母、中文，数字
        return check_input_str(s, min_len=3, max_len=50, letters=True, chinese=True, numbers=True)
