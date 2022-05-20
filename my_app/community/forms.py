# Aly Nour & Isabella Dube-Miglioli

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user
from my_app import photos
from my_app.models import Profile, User


class BlogForm(FlaskForm):
    answer_1 = StringField(label='How do you feel about your country\'s emissions?',
                           validators=[DataRequired(message='Answer required.')])
    answer_2 = SelectField(label='How likely are you to contribute in reducing those emissions?',
                           choices=[x for x in range(0, 10)],
                           validators=[DataRequired(message='Answer required.')])
    answer_3 = StringField(label='What\'s your opinion on your government\'s stance about greenhouse gases?',
                           validators=[DataRequired(message='Answer required.')])
    answer_4 = SelectField(label='How much do you know about your country\'s emissions?',
                           choices=[x for x in range(0, 10)],
                           validators=[DataRequired(message='Answer required.')])


class ProfileForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(message='Username is required.')])
    bio = TextAreaField(label='Bio', description="Tell the world about yourself")
    age = SelectField(label='Age range', validators=[DataRequired(message='Age is required.')],
                      choices=['Under 12', '12 to 17', '18 to 24', '25 to 34', '35 to 44', '45 to 54', '55 to 64',
                               '65 to 74', '75 and older'])
    region = SelectField(label='Preferred region', validators=[DataRequired(message='Preferred region is required.')],
                         choices=['EU', 'Southern Europe', 'Italy',
                                  'Spain'])
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only.')])

    def validate_photo(self, photo):
        if photo is None:
            photo = 'static/img/User_icon.PNG'
            Profile.photo = photo

    def validate_username(self, username):
        profile = Profile.query.filter_by(username=username.data).first()
        current_profile = Profile.query.join(User).filter_by(id=current_user.id).first()
        if profile is not None:
            if profile is not current_profile:
                raise ValidationError('This user name is already in use, please choose a different user name.')
        elif len(username.data) < 8:
            raise ValidationError('Username characters must be greater than 8')
        elif len(username.data) > 12:
            raise ValidationError('Username characters must be less than 12')
