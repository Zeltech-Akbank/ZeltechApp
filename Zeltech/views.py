from flask import render_template
from flask_socketio import SocketIO
from . import chat

from .controllers import Settings, ChatSession, RequestManager

socketio = SocketIO(cors_allowed_origins="*")

settings = Settings()
chat_session = ChatSession()
manager = RequestManager(settings, chat_session)


@chat.route('/')
def index():
    return render_template('chat.html')


@socketio.on('user_message')
def handle_user_message(message):
    print("Message received:", message)
    
    try:
        bot_response = manager.send_request(message)
    except ConnectionError:
        bot_response = "Bir hata oluştu. Lütfen tekrar deneyin."
    
    socketio.emit('bot_response', bot_response)
