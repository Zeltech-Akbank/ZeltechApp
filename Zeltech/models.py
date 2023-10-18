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