from functools import wraps
from flask import g, request, current_app
from app.models.user import UserModel
from app.services.response import res_json
from app.utils.helpers import verifty_jwt_token, genrate_jwt_token


def api_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Api-Token')
        if token is None or token.strip() == '':
            return res_json(code='token_missing')

        token = verifty_jwt_token(token, current_app.config.get("SECRET_KEY"), current_app.config.get("USER_VALIDITY"))
        user = UserModel.get_model_by_fields(api_token=token)
        if user is None:
            return res_json(code='invalid_token')

        # 设置user
        g.user = user
        response = func(*args, **kwargs)
        if user.api_token:
            response.headers["api_token"] = genrate_jwt_token(user.api_token, current_app.config.get("SECRET_KEY"), current_app.config.get("USER_VALIDITY"))
        return response

    return wrapper



