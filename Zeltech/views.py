from flask import render_template
from flask_socketio import SocketIO
from . import chat

socketio = SocketIO(cors_allowed_origins="*")


@chat.route('/')
def index():
    return render_template('chat.html')


@socketio.on('user_message')
def handle_user_message(message):
    print("Message received:", message)
    bot_response = f"Onu söyleyemiyoruz maalesef.-*-{message}-*-"
    socketio.emit('bot_response', bot_response)
