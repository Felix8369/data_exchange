from app import create_app
from app.settings import DefaultConfig

application = create_app(DefaultConfig)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
