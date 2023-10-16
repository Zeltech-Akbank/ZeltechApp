from flask import Flask
from flask_cors import CORS
from decouple import config as cf
from Zeltech import chat
from Zeltech.views import socketio


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = cf('SECRET_KEY')
    app.config.from_object('config')

    app.register_blueprint(chat)

    socketio.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    socketio.run(app, port=5001, debug=True)
