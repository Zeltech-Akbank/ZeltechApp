import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()


class UserRole(enum.Enum):
    AFAD_YETKILISI = "AFAD_YETKILISI"
    AFAD_GONULLUSU = "AFAD_GONULLUSU"
    STK_UYESI = "STK_UYESI"


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'{self.username}'


class FormEntry(db.Model):
    __tablename__ = 'form_entries'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    sender_name = db.Column(db.String(255), nullable=False)  # gonderici_adi
    driver_id_number = db.Column(db.String(11), nullable=False)  # sofor_tckn
    sender_phone = db.Column(db.String(20), nullable=False)  # gonderici_telefonu
    driver_name = db.Column(db.String(255), nullable=False)  # sofor_adi
    driver_mobile_phone = db.Column(db.String(20), nullable=False)  # sofor_cep_telefonu
    license_plate = db.Column(db.String(10), nullable=False)  # plaka
    assistance_status = db.Column(db.String(50), nullable=False)  # yardim_durumu
    dispatch_province = db.Column(db.String(50), nullable=False)  # gonderim_il
    dispatch_district = db.Column(db.String(50), nullable=False)  # gonderim_ilce
    dispatch_date = db.Column(db.Date, nullable=False)  # gonderim_tarihi
    dispatch_note = db.Column(db.Text)  # gonderim_not
    delivery_province = db.Column(db.String(50), nullable=False)  # teslimat_il
    delivery_district = db.Column(db.String(50), nullable=False)  # teslimat_ilce
    estimated_delivery_date = db.Column(db.Date, nullable=False)  # tahmini_teslimat_tarihi
    delivery_note = db.Column(db.Text)  # teslimat_not

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AidsOnVehicle(db.Model):
    __tablename__ = 'aids_on_vehicle'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    form_entry_id = db.Column(UUID(as_uuid=True), db.ForeignKey('form_entries.id'), nullable=False)  # form_entry_id
    aid_type = db.Column(db.String(50), nullable=False)  # yardim_tipi
    aid_quantity = db.Column(db.Integer, nullable=False)  # yardim_miktar
    size = db.Column(db.String(20))  # beden

    form_entry = db.relationship('FormEntry', backref=db.backref('aids_on_vehicle', lazy=True))


class HelpType(db.Model):
    __tablename__ = 'help_type'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'description': self.description
        }


class Size(db.Model):
    __tablename__ = 'size'

    id = db.Column(db.Integer, primary_key=True)
    size_type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False, server_default="",
                         server_check=db.text("category IN ('male-female', 'child')"))


class City(db.Model):
    __tablename__ = 'cities'

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(255), nullable=False)
    districts = db.relationship('District', backref='city', lazy=True)


class District(db.Model):
    __tablename__ = 'districts'

    district_id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=False)
    district_name = db.Column(db.String(255), nullable=False)


class Tweets(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    tweet_content = db.Column(db.Text)
    tag = db.Column(db.Text)
    tweet_parser_json = db.Column(db.JSON)
    city = db.Column(db.Text)
    distincts = db.Column(db.Text)
    neighbourhood = db.Column(db.Text)
    phone = db.Column(db.Text)
    address = db.Column(db.Text)
    street_road = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    come_true = db.Column(db.Boolean, default=False) #ihtiyaç karşılandı.
    confirmation = db.Column(db.Boolean, default=False) #teyit edildi.
