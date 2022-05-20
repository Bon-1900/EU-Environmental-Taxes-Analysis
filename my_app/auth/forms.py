# Aly Nour & Isabella Dube-Miglioli & Yuansheng zhang

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask import request
from werkzeug.datastructures import CombinedMultiDict

from my_app.models import User


class SignupForm(FlaskForm):
    title = SelectField(label='Title', choices=['Mr', 'Mrs', 'Dr', 'Ms'])
    first_name = StringField(label='First name', validators=[DataRequired()])
    last_name = StringField(label='Last name', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired()])

    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    security_question = SelectField(label='security question', choices=['What\'s your mother\'s maiden name?',
                                                                        'What\'s the name of your favourite teacher?',
                                                                        'What was the name of your first pet?',
                                                                        'What\'s the make of your first?'])
    security_answer = StringField(label='Security answer', validators=[DataRequired()])


    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')


    def validate_password(form, field):
        if len(field.data) < 8:
            raise ValidationError('Password must be greater than 8')
        elif len(field.data) > 12:
            raise ValidationError('Password must be less than 12')



class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('The email address indicated is not registered')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            return None
        if not user.check_password(password.data):
            raise ValidationError('The password is not valid')


class SecurityForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('The email address indicated is not registered')

    security_question = SelectField(label='Security question', choices=['What\'s your mother\'s maiden name?',
                                                                        'What\'s the name of your favourite teacher?',
                                                                        'What was the name of your first pet?',
                                                                        'What\'s the make of your first?'])
    security_answer = StringField(label='Security answer', validators=[DataRequired()])

    def validate_security_answer(self, security_answer):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            return None
        if not user.security_answer_check(security_answer.data):
            raise ValidationError('Incorrect answer')


