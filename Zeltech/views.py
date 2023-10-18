from functools import wraps

from flask import current_app, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO
from . import chat, app, auth
from flask import jsonify
from .controllers import Settings, ChatSession, RequestManager
from .models import FormEntry, AidsOnVehicle, Users, db
from sqlalchemy import MetaData


socketio = SocketIO(cors_allowed_origins="*")

settings = Settings()
chat_session = ChatSession()
manager = RequestManager(settings, chat_session)


@app.route('/dbtest')
def dbtest():
    try:
        with current_app.app_context():
            # Bir sorgu çalıştırarak veritabanı bağlantısını test edin
            meta = MetaData()
            meta.reflect(bind=db.engine)
            tables = list(meta.tables.keys())
            return f"Bağlantı başarılı! Tablolar: {tables}"
    except Exception as e:
        return f"Bağlantı hatası: {str(e)}"


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


def admin_access_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if 'username' in session:
            return view_func(*args, **kwargs)
        else:
            flash('Admin paneline erişim izniniz yok.', 'danger')
            return redirect(url_for('login'))
    return decorated_view


@app.route('/admin_panel')
@admin_access_required
def admin_panel():
    username = session['username']
    return render_template('admin_panel.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user is not None and user.password == password:
            session['username'] = user.username  # Kullanıcının adını oturumda sakla
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('app.admin_panel'))
        else:
            flash('Hatalı kullanıcı adı veya şifre.', 'danger')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.clear()
    return redirect(url_for('app.login'))



@app.route('/logistic')
def logistic_template():
    data = {'a de bakalım': 'a', 'bide y de': 'y', 'şimdi bide ı': 'ı'}
    return render_template('logistics.html', veri=data)


@app.route('/form-submit', methods=['POST'])
def form_submit():
    gonderici_adi = request.form.get('gonderici-adi')
    sofor_tckn = request.form.get('sofor-tckn')
    gonderici_telefonu = request.form.get('gonderici-telefonu')

    sofor_adi = request.form.get('sofor-adi')
    sofor_cep_telefonu = request.form.get('sofor-cep-telefonu')
    plaka = request.form.get('plaka')
    yardim_durumu = request.form.get('yardim-durumu')

    gonderim_il = request.form.get('gonderim-il')
    gonderim_ilce = request.form.get('gonderim-ilce')
    gonderim_tarihi = request.form.get('gonderim-tarihi')
    gonderim_not = request.form.get('gonderim-not')

    teslimat_il = request.form.get('teslimat-il')
    teslimat_ilce = request.form.get('teslimat-ilce')
    tahmini_teslimat_tarihi = request.form.get('tahmini-teslimat-tarihi')
    teslimat_not = request.form.get('teslimat-not')

    yardim_tipi = request.form.getlist('yardim-tipi[]')
    yardim_miktar = request.form.getlist('yardim-miktar[]')
    beden = request.form.getlist('beden[]')

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

@app.route('/logistic-review')
def logistics_review():
    entries = FormEntry.query.all()  # Tüm kayıtları al.
    if not entries:
        return "Veritabanında hiç veri bulunmamaktadır."

    data_list = []

    for entry in entries:
        aids_on_vehicle = AidsOnVehicle.query.filter_by(form_entry_id=entry.id).all()
        data = {
            "gonderici-adi": entry.sender_name,
            "sofor-tckn": entry.driver_id_number,
            "gonderici-telefonu": entry.sender_phone,
            "sofor-adi": entry.driver_name,
            "sofor-cep-telefonu": entry.driver_mobile_phone,
            "plaka": entry.license_plate,
            "yardim-durumu": entry.assistance_status,
            "gonderim-il": entry.dispatch_province,
            "gonderim-ilce": entry.dispatch_district,
            "gonderim-tarihi": entry.dispatch_date.strftime('%Y-%m-%d'),
            "gonderim-not": entry.dispatch_note,
            "teslimat-il": entry.delivery_province,
            "teslimat-ilce": entry.delivery_district,
            "tahmini-teslimat-tarihi": entry.estimated_delivery_date.strftime('%Y-%m-%d'),
            "teslimat-not": entry.delivery_note,
            "yardimlar": [
                {
                    "yardim-tipi": aid.aid_type,
                    "yardim-miktar": aid.aid_quantity,
                    "beden": aid.size or ""
                }
                for aid in aids_on_vehicle
            ]
        }
        data_list.append(data)

    return render_template('logistics_review.html', items=data_list)



ihbarlar = [{"isim": f"Örnek İsim {i}", "konu": "Örnek Konu", "detay": "Örnek Detay", "teyit": "Hayır",
                 "karsilandi": "Hayır", "id": i} for i in range(1, 3)]  # 50 örnek ihbar bu veritabanından gelcek.


@app.route('/maps')
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


@app.route('/durum-duzenle/<int:id>', methods=['POST'])
def duzenle(id):
    global ihbarlar
    for ihbar in ihbarlar:
        if ihbar['id'] == id:
            ihbar['teyit'] = request.form.get('teyit')
            ihbar['karsilandi'] = request.form.get('karsilandi')
            break

    print(ihbarlar)
    return jsonify({'status': 'success'})

