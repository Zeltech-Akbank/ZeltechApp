import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserRole(enum.Enum):
    AFAD_YETKILISI = "afad yetkilisi"
    AFAD_GONULLUSU = "afad gönüllüsü"
    STK_UYESI = "stk üyesi"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(UserRole), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class FormEntry(db.Model):
    __tablename__ = 'form_entries'

    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(255), nullable=False) # gonderici_adi
    driver_id_number = db.Column(db.String(11), nullable=False) # sofor_tckn
    sender_phone = db.Column(db.String(20), nullable=False) # gonderici_telefonu
    driver_name = db.Column(db.String(255), nullable=False) # sofor_adi
    driver_mobile_phone = db.Column(db.String(20), nullable=False) # sofor_cep_telefonu
    license_plate = db.Column(db.String(10), nullable=False) # plaka
    assistance_status = db.Column(db.String(50), nullable=False) # yardim_durumu
    dispatch_province = db.Column(db.String(50), nullable=False) # gonderim_il
    dispatch_district = db.Column(db.String(50), nullable=False) # gonderim_ilce
    dispatch_date = db.Column(db.Date, nullable=False) # gonderim_tarihi
    dispatch_note = db.Column(db.Text) # gonderim_not
    delivery_province = db.Column(db.String(50), nullable=False) # teslimat_il
    delivery_district = db.Column(db.String(50), nullable=False) # teslimat_ilce
    estimated_delivery_date = db.Column(db.Date, nullable=False) # tahmini_teslimat_tarihi
    delivery_note = db.Column(db.Text) # teslimat_not


class AidsOnVehicle(db.Model):
    __tablename__ = 'aids_on_vehicle'

    id = db.Column(db.Integer, primary_key=True)
    form_entry_id = db.Column(db.Integer, db.ForeignKey('form_entries.id'), nullable=False) # form_entry_id
    aid_type = db.Column(db.String(50), nullable=False) # yardim_tipi
    aid_quantity = db.Column(db.Integer, nullable=False) # yardim_miktar
    size = db.Column(db.String(20)) # beden

    form_entry = db.relationship('FormEntry', backref=db.backref('aids_on_vehicle', lazy=True))

