from flask import render_template, request
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


@chat.route('/logistic')
def logistic_template():
    data = {'a de bakalım': 'a', 'bide y de': 'y', 'şimdi bide ı': 'ı'}
    return render_template('logistics.html', veri=data)


@chat.route('/form-submit', methods=['POST'])
def form_submit():
    # Gönderen Bilgileri
    gonderici_adi = request.form.get('gonderici-adi')
    sofor_tckn = request.form.get('sofor-tckn')
    gonderici_telefonu = request.form.get('gonderici-telefonu')

    # Araç Bilgileri
    sofor_adi = request.form.get('sofor-adi')
    sofor_cep_telefonu = request.form.get('sofor-cep-telefonu')
    plaka = request.form.get('plaka')
    yardim_durumu = request.form.get('yardim-durumu')

    # Gönderim Adresi
    gonderim_il = request.form.get('gonderim-il')
    gonderim_ilce = request.form.get('gonderim-ilce')
    gonderim_tarihi = request.form.get('gonderim-tarihi')
    gonderim_not = request.form.get('gonderim-not')

    # Teslimat Adresi
    teslimat_il = request.form.get('teslimat-il')
    teslimat_ilce = request.form.get('teslimat-ilce')
    tahmini_teslimat_tarihi = request.form.get('tahmini-teslimat-tarihi')
    teslimat_not = request.form.get('teslimat-not')

    # Araçtaki Yardımlar
    yardim_tipi = request.form.getlist('yardim-tipi[]')  # Listeyi al
    yardim_miktar = request.form.getlist('yardim-miktar[]')  # Listeyi al
    beden = request.form.getlist('beden[]')  # Listeyi al

    # Verileri toplama
    data = {
        "Gönderen Bilgileri": {
            "Gönderici Adı": gonderici_adi,
            "Şoför TCKN": sofor_tckn,
            "Gönderici Telefonu": gonderici_telefonu
        },
        "Araç Bilgileri": {
            "Şoför Adı": sofor_adi,
            "Şoför Cep Telefonu": sofor_cep_telefonu,
            "Plaka": plaka,
            "Yardım Durumu": yardim_durumu
        },
        "Gönderim Adresi": {
            "İl": gonderim_il,
            "İlçe": gonderim_ilce,
            "Gönderim Tarihi": gonderim_tarihi,
            "Not": gonderim_not
        },
        "Teslimat Adresi": {
            "İl": teslimat_il,
            "İlçe": teslimat_ilce,
            "Tahmini Teslimat Tarihi": tahmini_teslimat_tarihi,
            "Not": teslimat_not
        },
        "Araçtaki Yardımlar": [{
            "Yardım Tipi": y_tipi,
            "Yardım Miktarı": y_miktar,
            "Beden": b
        } for y_tipi, y_miktar, b in zip(yardim_tipi, yardim_miktar, beden)]
    }

    print(data)
    # Daha sonra bu veriyi bir veritabanına kaydedeceğiz.
    return jsonify(data)


@chat.route('/logistic-review')
def logistics_review():
    mock_data = {
        "gonderici-adi": "Ahmet Yılmaz",
        "sofor-tckn": "12345678901",
        "gonderici-telefonu": "555 555 55 55",
        "sofor-adi": "Mehmet Öztürk",
        "sofor-cep-telefonu": "533 533 53 33",
        "plaka": "34 ABC 123",
        "yardim-durumu": "Yolda",
        "gonderim-il": "İstanbul",
        "gonderim-ilce": "Beşiktaş",
        "gonderim-tarihi": "2023-10-20",
        "gonderim-not": "Selçuklu Belediyesin’den İletilmekte…",
        "teslimat-il": "Ankara",
        "teslimat-ilce": "Çankaya",
        "tahmini-teslimat-tarihi": "2023-10-22",
        "teslimat-not": "Maraş Dokuz Eylül Dağıtım Merkezine Teslim Edilecektir…",
        "yardimlar": [
            {"yardim-tipi": "Çadır", "yardim-miktar": 2},
            {"yardim-tipi": "Battaniye", "yardim-miktar": 5},
            {"yardim-tipi": "Su", "yardim-miktar": 10},
            {"yardim-tipi": "Erkek Giysi", "yardim-miktar": 7, "beden": "L"},
            {"yardim-tipi": "Kadın İç Çamaşır", "yardim-miktar": 15, "beden": "M"},
            {"yardim-tipi": "Çocuk Giysisi", "yardim-miktar": 4, "beden": "3-6 Yaş"},
        ]
    }

    return render_template('logistics_review.html', items=mock_data)

ihbarlar = [{"isim": f"Örnek İsim {i}", "konu": "Örnek Konu", "detay": "Örnek Detay", "teyit": "Hayır",
                 "karsilandi": "Hayır", "id": i} for i in range(1, 3)]  # 50 örnek ihbar bu veritabanından gelcek.

@chat.route('/maps')
def maps_view():
    pois = [
        {"lat": 39.9334, "lng": 32.8597, "label": "Hastane", "info": "Hastane A - Acil Servis"},
        {"lat": 39.9335, "lng": 32.8598, "label": "Eczane", "info": "Eczane B - 24 Saat Açık"},
        {"lat": 39.9333, "lng": 32.8596, "label": "Park Alanı", "info": "Park C - Çocuk Oyun Alanı Mevcut"},
        {"lat": 39.9332, "lng": 32.8595, "label": "Veteriner", "info": "Veteriner D - Hayvan Bakımı"},
        {"lat": 39.9336, "lng": 32.8599, "label": "Okul", "info": "Okul E - İlköğretim"}
    ]

    # Sayfa numarasını al
    page = request.args.get('page', 1, type=int)
    items_per_page = 10


    total_ihbarlar = len(ihbarlar)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_ihbarlar = ihbarlar[start:end]

    return render_template('maps.html', pois=pois, ihbarlar=paginated_ihbarlar,
                           total_pages=(total_ihbarlar // items_per_page) + 1)


@chat.route('/durum-duzenle/<int:id>', methods=['POST'])
def duzenle(id):
    global ihbarlar
    for ihbar in ihbarlar:
        if ihbar['id'] == id:
            ihbar['teyit'] = request.form.get('teyit')
            ihbar['karsilandi'] = request.form.get('karsilandi')
            break

    print(ihbarlar)
    return jsonify({'status': 'success'})


@socketio.on('user_message')
def handle_user_message(message):
    print("Message received:", message)
    
    try:
        bot_response = manager.send_request(message)
    except ConnectionError:
        bot_response = "Bir hata oluştu. Lütfen tekrar deneyin."
    
    socketio.emit('bot_response', bot_response)
