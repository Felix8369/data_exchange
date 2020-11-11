from flask import Blueprint
from flask_restful import Api
from app.resources.auth import AuthLoginResource, AuthLogoutResource, AuthProfileResource


urls = Blueprint('urls', __name__)

api = Api(urls)

# 登录
api.add_resource(AuthLoginResource, '/v1/login')
api.add_resource(AuthLogoutResource, '/v1/logout')
api.add_resource(AuthProfileResource, '/v1/profile')
