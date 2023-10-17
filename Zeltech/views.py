from flask import render_template, request
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


@chat.route('/admin-panel')
def admin_panel():
    return render_template('admin_panel.html')


@chat.route('/logistic')
def logistic_template():
    data = {'a de bakalım': 'a', 'bide y de': 'y', 'şimdi bide ı': 'ı'}
    return render_template('logistics.html', veri=data)


@chat.route('/form-submit', methods=['POST'])
def form_submit():

    gonderici_adi = request.form.get('gonderici-adi')
    gonderici_telefonu = request.form.get('gonderici-telefonu')
    gonderim_tarihi = request.form.get('gonderim-tarihi')
    tahmini_teslimat_tarihi = request.form.get('tahmini-teslimat-tarihi')
    sofor_adi = request.form.get('sofor-adi')
    sofor_cep_telefonu = request.form.get('sofor-cep-telefonu')
    plaka = request.form.get('plaka')
    yardim_durumu = request.form.get('yardim-durumu')

    print(f'Gönderici Adı: {gonderici_adi}')
    print(f'Gönderici Telefonu: {gonderici_telefonu}')
    print(f'Gönderim Tarihi: {gonderim_tarihi}')
    print(f'Tahmini Teslimat Tarihi: {tahmini_teslimat_tarihi}')
    print(f'Şoför Adı: {sofor_adi}')
    print(f'Şoför Cep Telefonu: {sofor_cep_telefonu}')
    print(f'Plaka: {plaka}')
    print(f'Yardım Durumu: {yardim_durumu}')

    return render_template('admin_panel.html')


@chat.route('/logistic-review')
def logistics_review():
    # Örnek veri seti
    items = [
        {
            'gonderici_adi': 'Ahmet Yılmaz',
            'gonderici_telefonu': '555 555 55 55',
            'gonderim_tarihi': '2023-10-16',
            'tahmini_teslimat_tarihi': '2023-10-20',
            'sofor_adi': 'Mehmet Öz',
            'sofor_cep_telefonu': '533 533 53 33',
            'plaka': '34 ABC 123',
            'yardim_durumu': 'Yolda'
        },
        {
            'gonderici_adi': 'Elif Kaya',
            'gonderici_telefonu': '544 544 44 44',
            'gonderim_tarihi': '2023-10-15',
            'tahmini_teslimat_tarihi': '2023-10-19',
            'sofor_adi': 'Ayşe Taş',
            'sofor_cep_telefonu': '511 511 51 11',
            'plaka': '06 DEF 456',
            'yardim_durumu': 'Hazırlanıyor'
        }
    ]

    return render_template('logistics_review.html', items=items)


@chat.route('/maps')
def get_maps():
    return render_template('maps.html')


@socketio.on('user_message')
def handle_user_message(message):
    print("Message received:", message)
    
    try:
        bot_response = manager.send_request(message)
    except ConnectionError:
        bot_response = "Bir hata oluştu. Lütfen tekrar deneyin."
    
    socketio.emit('bot_response', bot_response)
