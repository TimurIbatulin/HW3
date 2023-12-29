from wtforms.validators import DataRequired, EqualTo, Regexp, Length, Email
from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm


class UserRegistration(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    surname = StringField('Surname', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20),
                                                     Regexp(r'(?=.*[a-zA-Z])(?=.*\d)',
                                                     message=
                                                     'Пароль должен содержать хотя бы одну букву и одну цифру')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
