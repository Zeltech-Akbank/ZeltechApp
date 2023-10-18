from flask import Flask
from flask_cors import CORS
from decouple import config as cf
from Zeltech import chat, app as app_blueprint
from Zeltech.views import socketio
from decouple import config
from Zeltech.models import db


def create_tables(app):
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = cf('SECRET_KEY')
    app.config.from_object('config')

    app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(chat)
    app.register_blueprint(app_blueprint)

    socketio.init_app(app)
    return app


if __name__ == '__main__':
    app_instance = create_app()
    #create_tables(app_instance)
    socketio.run(app_instance, port=5002, debug=True)
