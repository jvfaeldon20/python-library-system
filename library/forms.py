from flask.app          import Flask
from flask_wtf          import FlaskForm
from wtforms            import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from library.models     import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists! Please try a different email')

    username     = StringField(label='Username: ',validators=[Length(min=2,max=30), DataRequired()])
    email        = StringField(label='Email Address: ',validators=[Email(), DataRequired()])
    password1    = PasswordField(label='Password: ',validators=[Length(min=6), DataRequired()])
    password2    = PasswordField(label='Confirm Password: ',validators=[EqualTo('password1'), DataRequired()])
    user_type    = StringField(label='Type: ')
    submit       = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username     = StringField(label='Username: ', validators=[DataRequired()])
    password     = PasswordField(label='Password: ', validators=[DataRequired()])
    submit       = SubmitField(label='Sign In')


class BorrowBookForm(FlaskForm):
    submit       = SubmitField(label='Borrow Item!')


class AddBookForm(FlaskForm):
    title        = StringField(label='Title: ', validators=[DataRequired()])
    description  = StringField(label='Description: ', validators=[DataRequired()])
    genre        = StringField(label='Genre: ', validators=[DataRequired()])
    author       = StringField(label='Author: ', validators=[DataRequired()])
    stocks       = StringField(label='Author: ', validators=[DataRequired()])
    submit       = SubmitField(label='Save Book')
