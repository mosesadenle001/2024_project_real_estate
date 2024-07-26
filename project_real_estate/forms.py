
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from project_real_estate.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username has been used. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email has been used. Please choose a different one.')

class PromoteUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Promote to Admin')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username has been used. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email has been used. Please choose a different one.')

class LocationForm(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Location')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class CompareForm(FlaskForm):
    properties1 = SelectField('Properties 1', validators=[DataRequired()])
    properties2 = SelectField('Properties 2', validators=[DataRequired()])
    submit = SubmitField('Compare')

# class PropertyForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])
#     description = TextAreaField('Description', validators=[DataRequired()])
#     price = FloatField('Price', validators=[DataRequired()])
#     location = StringField('Location', validators=[DataRequired()])
#     submit = SubmitField('Post Property')

class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Update Property')
class SubmitPropertiesForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[DataRequired()])
    bathrooms = IntegerField('Bathrooms', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit Properties')
class SearchForm(FlaskForm):
    search_query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class DeleteForm(FlaskForm):
    pass


