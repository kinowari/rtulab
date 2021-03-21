from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import Required, DataRequired


class LoginForm(FlaskForm):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField()

