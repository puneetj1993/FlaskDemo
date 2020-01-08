from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length,Email,EqualTo,ValidationError
from flask_package.models import User
from flask import flash

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=14)])
    confirm = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('Username already exists')
            raise ValidationError()

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('email already exists')
            raise ValidationError()
        
        

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=14)])
    submit = SubmitField('Sign In')
    remember_me = BooleanField('Remember me')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            flash("email doesn't exists. Please register yourself by clicking on the below link")
            raise ValidationError()
