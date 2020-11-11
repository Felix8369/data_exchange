from flask import Flask
from app.routes import urls
from app.services.response import res_json


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # DB
    from app.models import db
    db.init_app(app)

    @app.errorhandler(404)
    @app.errorhandler(405)
    def not_found_handler(e):
        return res_json(code='not_found'), 404

    @app.errorhandler(Exception)
    def system_error_handler(e):
        app.logger.exception(e)
        return res_json(code='system_error'), 500

    # Router
    app.register_blueprint(urls)

    # APScheduler
    # from app.services.scheduler import scheduler_init
    # scheduler_init(app)

    return app
