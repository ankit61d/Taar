# from datetime import datetime
from taar_app import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.Integer(10), unique = True, nullable=False)

    def __repr__(self) -> str:
        return f"User('{self.id}', '{self.full_name}', '{self.phone_number}')"

