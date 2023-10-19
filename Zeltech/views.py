from functools import wraps

from flask import current_app, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO
from . import chat, app
from flask import jsonify
from .controllers import Settings, ChatSession, RequestManager
from .models import FormEntry, AidsOnVehicle, Users, db, HelpType, Size, City, District, Tweets
from sqlalchemy import MetaData, and_
import logging
logging.basicConfig(level=logging.DEBUG)

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
    user_role = session['user_role']
    return render_template('admin_panel.html', username=username, user_role=user_role)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user is not None and user.password == password:
            session['username'] = user.username  # Kullanıcının adını oturumda sakla
            session['user_role'] = " ".join(str(user.role).split('.')[1].split('_'))  # Kullanıcının adını oturumda sakla

            flash('Giriş başarılı!', 'success')
            return redirect(url_for('app.admin_panel'))
        else:
            flash('Hatalı kullanıcı adı veya şifre.', 'danger')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('user_role', None)

    session.clear()
    return redirect(url_for('app.login'))


@app.route('/logistic')
def logistic_template():
    help_types = HelpType.query.all()
    help_types_serializable = [ht.to_dict() for ht in help_types]
    sizes = Size.query.all()

    cities = City.query.all()
    districts = {city.city_name: District.query.filter_by(city_id=city.city_id).all() for city in cities}

    return render_template('logistics.html', help_types=help_types, sizes=sizes,
                           help_types_serializable=help_types_serializable, cities=cities, districts=districts)


@app.route('/form-submit', methods=['POST'])
def form_submit():
    try:
        form_entry = FormEntry(
            sender_name=request.form['gonderici-adi'],
            driver_id_number=request.form['sofor-tckn'],
            sender_phone=request.form['gonderici-telefonu'],
            driver_name=request.form['sofor-adi'],
            driver_mobile_phone=request.form['sofor-cep-telefonu'],
            license_plate=request.form['plaka'],
            assistance_status=request.form['yardim-durumu'],
            dispatch_province=request.form['gonderim-il'],
            dispatch_district=request.form['gonderim-ilce'],
            dispatch_date=request.form['gonderim-tarihi'],
            dispatch_note=request.form['gonderim-not'],
            delivery_province=request.form['teslimat-il'],
            delivery_district=request.form['teslimat-ilce'],
            estimated_delivery_date=request.form['tahmini-teslimat-tarihi'],
            delivery_note=request.form['teslimat-not']
        )

        db.session.add(form_entry)
        db.session.commit()

        form_entry_id = form_entry.id

        yardim_tipi = request.form.getlist('yardim-tipi[]')
        yardim_miktar = request.form.getlist('yardim-miktar[]')
        beden = request.form.getlist('beden[]')

        for tip, miktar, bed in zip(yardim_tipi, yardim_miktar, beden):
            # Eğer yardım tipi 'Çadır' veya başka bir bedensiz ürün ise bedeni atla.
            if tip not in ['Erkek Giysi', 'Erkek İç Çamaşır', 'Kadın Giysi', 'Kadın İç Çamaşır', 'Çocuk Giysisi', 'Çocuk İç Çamaşır']:
                bed = None

            aid = AidsOnVehicle(form_entry_id=form_entry_id, aid_type=tip, aid_quantity=miktar, size=bed)
            db.session.add(aid)

        db.session.commit()

        return jsonify({"message": "Success!", "redirect_url": "/admin_panel"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


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



@app.route('/maps')
def maps_view():
    # Query only those tweets where both city and distincts are not null
    # and tag is not "Alaksız İhbar"
    tweets = Tweets.query.filter(
        and_(
            Tweets.city.isnot(None),
            Tweets.city != 'nan',
            Tweets.distincts.isnot(None),
            Tweets.distincts != 'nan',
            Tweets.tag != 'Alaksız İhbar'
        )
    ).all()

    pois = []
    for tweet in tweets:
        pois.append({
            "lat": tweet.latitude,
            "lng": tweet.longitude,
            "label": tweet.tag,  # Tag'ı label olarak kullandım
            "info": tweet.tweet_content
        })

    return render_template('maps.html', pois=pois)


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

