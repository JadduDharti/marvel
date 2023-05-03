from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, DecimalField, DateField
from wtforms.validators import DataRequired, Email


class UserLoginForms(FlaskForm):
    #email, password, submit_button

    firstname = StringField('First Name', validators = [DataRequired()])
    lastname = StringField('Last Name', validators = [DataRequired()])
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    date_of_birth = DateField('Date of Birth (YYYY-MM-DD)', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()]) #, EqualTo('confirm_password', message='Passwords must match')])
    #confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit_button = SubmitField()


class MarvelCharacterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    comics_appeared_in = IntegerField('Comics Appeared In', validators=[DataRequired()])
    super_power = StringField('Super Power', validators=[DataRequired()])
    image_url = StringField('Image Url')
    submit_button = SubmitField('Submit')
