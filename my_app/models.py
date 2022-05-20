# Aly Nour & Isabella Dube-Miglioli

from flask_login import UserMixin
from my_app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Uncomment the following line and remove all the field definitions if you want to experiment with reflection"""
    # __table__ = db.Model.metadata.tables['user']

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    security_answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.firstname} {self.lastname}  {self.email} {self.password} {self.security_answer}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def security_answer_check(self, security_answer):
        return self.security_answer == security_answer


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    photo = db.Column(db.Text)
    bio = db.Column(db.Text)
    age = db.Column(db.Text)
    region = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    answer_1 = db.Column(db.Text, nullable=False)
    answer_2 = db.Column(db.Text, nullable=False)
    answer_3 = db.Column(db.Text, nullable=False)
    answer_4 = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
