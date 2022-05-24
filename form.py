from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField(label="Enter username", validators=[DataRequired(), Length(min=6, max=20)])
    password=PasswordField(label="Enter password", validators=[DataRequired(), Length(min=8, max=16)])
    submit=SubmitField(label="Login")

class RegisterForm(FlaskForm):
    first_name = StringField(label="Enter first name", validators=[DataRequired(), Length(min=1, max=20)])
    last_name = StringField(label="Enter last name", validators=[DataRequired(), Length(min=1, max=20)])
    email=StringField(label="Enter email", validators=[DataRequired(), Email()])
    username = StringField(label="Enter username", validators=[DataRequired(), Length(min=6, max=20)])
    password=PasswordField(label="Enter password", validators=[DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField(label="Confirm password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="Register")
