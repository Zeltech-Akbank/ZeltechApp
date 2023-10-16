from flask import render_template
from flask_socketio import SocketIO
from . import chat
from flask import jsonify

from .controllers import Settings, ChatSession, RequestManager

socketio = SocketIO(cors_allowed_origins="*")

settings = Settings()
chat_session = ChatSession()
manager = RequestManager(settings, chat_session)


@chat.route('/')
def index():
    return render_template('chat.html')


@chat.route('/admin-panel')
def admin_panel():
    return render_template('admin_panel.html')


@chat.route('/menu1_content')
def menu1_content():
    # Verileri işleyip, template'i döndür
    content = render_template('menu1.html', veri={'key':'value'}) # Örnek veri
    return jsonify({'html': content})


@chat.route('/menu2_content')
def menu2_content():
    content = render_template('menu2.html', veri={'key':'value'})
    return jsonify({'html': content})


@chat.route('/logistic')
def logistic_template():
    veri = {'a':'a de bakalım', 'b':'b de bakalım'}
    return render_template('logistics.html', veri=veri)


@socketio.on('user_message')
def handle_user_message(message):
    print("Message received:", message)
    
    try:
        bot_response = manager.send_request(message)
    except ConnectionError:
        bot_response = "Bir hata oluştu. Lütfen tekrar deneyin."
    
    socketio.emit('bot_response', bot_response)

