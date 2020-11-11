from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.services.response import res_json
from app.services.decorators import api_auth


class BaseResource(Resource):
    def __init__(self):
        self.parser = RequestParser(bundle_errors=True)

    def parse_args(self):
        """
        解析参数
        :return:
        """

        try:
            args = self.parser.parse_args()
            return args
        except Exception as e:
            e.data = res_json(code='param_error', ret_json=True)
            raise e

    def parse_pagination(self):
        """
        解析分页参数
        :return:
        """

        self.parser.add_argument('current_page', type=int, location='args', default=1)
        self.parser.add_argument('per_page', type=int, location='args', default=10, choices=range(1, 101))


class ApiResource(BaseResource):
    """
    Api token 资源
    """

    method_decorators = [api_auth]






